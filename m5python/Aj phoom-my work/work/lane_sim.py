from dataclasses import dataclass
from typing import Tuple, Optional
import math
import numpy as np
import cv2

@dataclass
class LaneSimConfig:
    width: int = 960
    height: int = 540
    fps: float = 60.0

    # Road shape / perspective
    curve_amplitude: float = 120.0
    curve_wavelength: float = 320.0

    horizon_y_ratio: float = 0.45
    top_y_ratio: float = 0.58

    lane_half_bottom: float = 240.0
    lane_half_top: float = 70.0

    road_extra_bottom: float = 260.0
    road_extra_top: float = 90.0

    # Driving dynamics
    base_speed: float = 180.0
    speed_min: float = 40.0
    speed_max: float = 520.0
    accel: float = 220.0
    brake: float = 320.0
    friction: float = 60.0

    steer_rate: float = 1.9
    steer_damp: float = 2.4
    lat_gain: float = 520.0 
    lat_damp: float = 3.2
    yaw_gain: float = 0.35
    yaw_damp: float = 1.8

    manual_nudge: float = 320.0
    # Scoring
    checkpoint_interval_px: float = 260.0

    # Colors (BGR for OpenCV)
    sky: Tuple[int,int,int] = (255, 200, 160)
    grass: Tuple[int,int,int] = (60, 150, 60)
    road: Tuple[int,int,int] = (55, 50, 50)
    white: Tuple[int,int,int] = (250, 250, 250)
    yellow: Tuple[int,int,int] = (120, 220, 255)

    CURVE2_AMPLITUDE = 70           
    CURVE2_WAVELENGTH = 140         
    CURVE_SWAY_RATE = 0.003
    CURVE_SWAY_GAIN = 0.6  

class LaneSim:
    def __init__(self, width: int = 960, height: int = 540, config: Optional[LaneSimConfig] = None):
        self.cfg = config or LaneSimConfig(width=width, height=height)
        self.W = self.cfg.width
        self.H = self.cfg.height
        self.FDT = 1.0 / self.cfg.fps

        # Derived positions
        self.HORIZON_Y = int(self.H * self.cfg.horizon_y_ratio)
        self.TOP_Y = int(self.H * self.cfg.top_y_ratio)
        self.BOTTOM_Y = self.H - 1

        self.reset()

        # Pre-allocate canvas
        self._canvas = np.zeros((self.H, self.W, 3), dtype=np.uint8)

    # --------- Public API ---------
    def reset(self):
        self.scroll = 0.0
        self.cam_x = 0.0
        self.lat_vel = 0.0
        self.steer = 0.0
        self.yaw = 0.0
        self.speed = self.cfg.base_speed
        self.survived = 0.0
        self.offlane = 0.0
        # scoring state
        self.score = 0
        self._next_cp = self.cfg.checkpoint_interval_px
        self._prev_on_lane = True
        self._last_event = ""  
        self._event_timer = 0.0

    def step(self, action: int = 0, dt: Optional[float] = None) -> np.ndarray:
        if dt is None:
            dt = self.FDT

        # --- Input to steering ---
        a = max(-1, min(1, int(action)))
        # แปลงเป็นแรงบิดพวงมาลัยแบบต่อเนื่อง
        self.steer += (a * self.cfg.steer_rate) * dt
        self.steer -= self.steer * self.cfg.steer_damp * dt

        # Lateral inertia
        lat_target = self.steer * self.cfg.lat_gain
        lat_acc = (lat_target - self.lat_vel) * self.cfg.lat_damp
        self.lat_vel += lat_acc * dt
        self.cam_x += self.lat_vel * dt

        # Manual nudge (ให้รู้สึกตอบสนอง)
        if a != 0:
            self.cam_x += (self.cfg.manual_nudge * a) * dt

        # Yaw follows steering
        self.yaw += (self.steer * self.cfg.yaw_gain - self.yaw) * self.cfg.yaw_damp * dt

        # Forward motion 
        self.scroll += self.speed * dt

        # --- Geometry ---
        c_bot = self._lane_center_x(self.BOTTOM_Y, self.scroll) - self.cam_x
        c_top = self._lane_center_x(self.TOP_Y, self.scroll) - self.cam_x + (self.yaw * 140.0)

        lb, rb = c_bot - self.cfg.lane_half_bottom, c_bot + self.cfg.lane_half_bottom
        lt, rt = c_top - self.cfg.lane_half_top,  c_top + self.cfg.lane_half_top

        road_half_bottom = self.cfg.lane_half_bottom + self.cfg.road_extra_bottom
        road_half_top = self.cfg.lane_half_top + self.cfg.road_extra_top
        rlb, rrb = c_bot - road_half_bottom, c_bot + road_half_bottom
        rlt, rrt = c_top - road_half_top,  c_top + road_half_top

        lane_poly = np.array([
            [int(lb), self.BOTTOM_Y], [int(lt), self.TOP_Y],
            [int(rt), self.TOP_Y],    [int(rb), self.BOTTOM_Y]
        ], dtype=np.int32)
        road_poly = np.array([
            [int(rlb), self.BOTTOM_Y], [int(rlt), self.HORIZON_Y],
            [int(rrt), self.HORIZON_Y], [int(rrb), self.BOTTOM_Y]
        ], dtype=np.int32)

        # On-lane check
        on_lane = (lb + 10) <= (self.W / 2) <= (rb - 10)
        if on_lane:
            self.survived += dt
        else:
            self.offlane += dt

        # Decrease event timer
        if self._event_timer > 0:
            self._event_timer = max(0.0, self._event_timer - dt)

        # --- Render ---
        img = self._canvas
        img[:] = self.cfg.sky 
        cv2.rectangle(img, (0, self.HORIZON_Y), (self.W-1, self.H-1), self.cfg.grass, -1)
        cv2.fillPoly(img, [road_poly], self.cfg.road)

        # Lane edges (solid white) with perspective thickness
        self._draw_tapered_line(img, self.cfg.white, (int(rlb), self.BOTTOM_Y), (int(rlt), self.HORIZON_Y), 12, 6)
        self._draw_tapered_line(img, self.cfg.white, (int(rrb), self.BOTTOM_Y), (int(rrt), self.HORIZON_Y), 18, 8)

        # Center dashed line (white/yellowish)
        center_bottom = ((int(rlb + rrb) // 2), self.BOTTOM_Y)
        center_top    = ((int(rlt + rrt) // 2), self.HORIZON_Y)
        self._draw_tapered_dashed(img, self.cfg.white, center_bottom, center_top, 10, 4, dash_len=36, gap_len=28)
        hud_text = f"spd:{int(self.speed)}  on:{self.survived:4.1f}s off:{self.offlane:4.1f}s"
        self._put_hud(img, hud_text, org=(12, 18))

        return img.copy() 

    # --------- Helpers ---------
    def _lane_center_x(self, screen_y: float, scroll: float) -> float:
        return self.W / 2 + self.cfg.curve_amplitude * math.sin((screen_y + scroll) / self.cfg.curve_wavelength)

    @staticmethod
    def _lerp(a: float, b: float, t: float) -> float:
        return a + (b - a) * t

    def _draw_tapered_line(self, img, color, p0, p1, w0, w1):
        x0, y0 = p0; x1, y1 = p1
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        if L < 1:
            return
        nx, ny = -dy / L, dx / L
        p0a = (int(x0 + nx * w0/2), int(y0 + ny * w0/2))
        p0b = (int(x0 - nx * w0/2), int(y0 - ny * w0/2))
        p1a = (int(x1 + nx * w1/2), int(y1 + ny * w1/2))
        p1b = (int(x1 - nx * w1/2), int(y1 - ny * w1/2))
        cv2.fillConvexPoly(img, np.array([p0a, p1a, p1b, p0b], dtype=np.int32), color)

    def _draw_tapered_dashed(self, img, color, p0, p1, w0, w1, dash_len=34, gap_len=26):
        x0, y0 = p0; x1, y1 = p1
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        if L < 1:
            return
        ux, uy = dx / L, dy / L
        step = dash_len + gap_len
        n = int(L // step) + 1
        for i in range(n):
            st = i * step
            ed = min(st + dash_len, L)
            if ed <= st:
                continue
            t0 = st / L
            t1 = ed / L
            sx, sy = int(x0 + ux * st), int(y0 + uy * st)
            ex, ey = int(x0 + ux * ed), int(y0 + uy * ed)
            ww0 = self._lerp(w0, w1, t0)
            ww1 = self._lerp(w0, w1, t1)
            self._draw_tapered_line(img, color, (sx, sy), (ex, ey), ww0, ww1)

    def _put_hud(self, img, text: str, org=(10, 20), color=(240, 240, 240)):
        cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 1, cv2.LINE_AA)

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel('m5python/Aj phoom-my work/work/spotify-2023.xlsx')

name=df.Track[0:101]
pop=df.Spotify_Popularity[0:101]

protitle={'size':15,'color':'darkviolet','backgroundcolor':'lavenderblush'}
data={'size':12,'color':'darkorange'}
plt.bar(name,pop,color = 'lightpink')

plt.ylim(80,100)
plt.xticks(fontsize=5)
plt.xticks(rotation=45, ha='right')

plt.xlabel('Name song',data,loc='right')
plt.ylabel('Popuraity',data)
plt.title('Top 100 Most Popular Spotify Song 2024',protitle,loc='center')
plt.savefig("matplot.png")
plt.show()
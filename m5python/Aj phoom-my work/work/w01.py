import pandas as pd
df = pd.read_excel('Product.xlsx')
match_product = df[df['product'].str.contains(input("Enter the product you want : "), na=False, case=False)]

if not match_product.empty:
    print(match_product)
    input_amount=int(input("Enter the amount of products you want : "))

    idx=match_product.index[0]
    
    if df.at[idx,'amount'] >= input_amount:
        total_price = df.at[idx,'price'] * input_amount

        df.at[idx,'amount'] -= input_amount

        df.to_excel('Product.xlsx',index=False)

        print(f'Total price : {total_price}')
        print(f"Amount of products after purchase : {df.at[idx, 'amount']}")
        
    
    else:
        print("Sorry,There is not enough product")
else:
    print("Dodn't find the product you wanted.")


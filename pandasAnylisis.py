import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




class InvoiceData:
    def __init__(self, df ):
        self.df = df
        self.df['TotalPrice'] = self.df['Quantity'] * self.df['Price']
        
    @property
    def revenue(self): # esta propiedad va a calcular el revenue total de la empresa
        # create temporary year/month columns so pivot_table can use column names
        df2 = self.df.copy()
        df2['Year'] = df2['InvoiceDate'].dt.year
        df2['Month'] = df2['InvoiceDate'].dt.month
        
 
        s = df2.pivot_table(
            columns='Year',
            index='Month',
            values='TotalPrice',
            fill_value=0,
            aggfunc='sum',
        )
        s.index = s.index.map(lambda month:pd.to_datetime(f'2024-{month}-01').strftime('%b') )
        return pd.DataFrame({
            'Month' : s.index,
            2009 : s[2009] ,
            2010 : s[2010] , 
            2011 : s[2011]
        })
    
    @property 
    def revenueTable(self):
        # create temporary year/month columns so pivot_table can use column names
        df2 = self.df.copy()
        df2['Year'] = df2['InvoiceDate'].dt.year
        df2['Month'] = df2['InvoiceDate'].dt.month
        
 
        s = df2.pivot_table(
            columns='Year',
            index='Month',
            values='TotalPrice',
            fill_value=0,
            aggfunc='sum',
        )
        s.index = s.index.map(lambda month:pd.to_datetime(f'2024-{month}-01').strftime('%b') )
        return s
    
    @property # esta propiedad va a devolver los paises que mas compran
    def revenue_countries(self): 
        s = self.df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False)
        return  pd.DataFrame({
            "Countries" : pd.Series(s.index).astype(str), # para categorias se tiene que pasar a str
            "Revenue": s.values,
        })
     
    @property    
    def revenue_products(self):
        # hacemos una copia del dataframe
        s = self.df.copy()
        # este groupby va a agrupar por porducto y va a sumar la cantidad comprada
        # y el total recaudado
        df_products = (
        s.groupby('StockCode')[['Quantity' , 'TotalPrice']]
        .sum()
        ).sort_values('TotalPrice' , ascending=False).head(20) 
        # te los ordena y muestra los 10 primeros
        
        s.index = s['StockCode'] # el dataframe original se le modifica el indice
        
        priceUnit = []
        for i in list(df_products.index): # buscamos por indice la fila entera del producto
            priceUnit.append(s.loc[i]['Price'].mean())
            #se saca el promedio del precio unitario y se lo almacena
            
        
        d = pd.DataFrame({
            "Product": df_products.index,
            "Quantity": list(df_products['Quantity']),
            "Mean Price": priceUnit,
            "Total Revenue": list(df_products['TotalPrice'])
        } , index=df_products.index)
        return d
    
    @property
    def revenue_days(self):
        # dataFrame para almacenar la columna de dias
        df_days = self.df.copy()
        df_days['Days'] = df_days['InvoiceDate'].dt.day_name()
        # aca hacemos el group by con la tabla de apoyo de dias
        s = df_days.groupby('Days')['TotalPrice'].sum()
        s.sort_index(ascending = True)
        return pd.DataFrame({
            'Days': s.index ,
            'Revenue': s.values
        })
    
    @property
    def revenue_customer (self):
        s = self.df.copy()
        c = s.groupby('Customer ID')['TotalPrice'].sum().sort_values(ascending=False).head(10)
        
        # obtenemos el ultimo dia de compra de cada cliente para ponerlo como indice del dataframe final
        s.index = s['Customer ID']
        lastPurchase = []
        # busca por indice el ultimo dia de compra de cada cliente que saque en el broupby
        for i in list(c.index): lastPurchase.append(s.loc[i]['InvoiceDate'].max())
        c.index = c.index.astype('category')
        d = pd.DataFrame({
            'Customer' : c.index,
            'Last Purchase Date': lastPurchase,
            'Total Revenue': list(c.values)
        })
        return d
        



def limpiar_df(df):
    df = df[df['Customer ID'].isna() == False] # limpia la tabla de los valores nulos en el customer id
    df = df[df['Quantity'] > 0] # limpia la tabla de los valores negativos de quantity
    pd.options.display.float_format = '{:.2f}'.format 
    df['Customer ID'] = df['Customer ID'].astype(int)
    return df


# el siguiente bloque solo se ejecuta cuando el módulo se corre directamente
# y no al importarlo desde otro archivo.
if __name__ == "__main__":
    df = pd.read_csv('online_retail.csv' , parse_dates=['InvoiceDate'] , dtype={
        "Customer ID": "float32",
        "Quantity": "int32",
        "Price": "float32",
        "Country": "category",
    })

    # sample para pruebas 
    sample = pd.read_csv('online_retail.csv' , nrows=5000)

    df = limpiar_df(df)

    # se instancia la clase DataFrame con el dataframe creado
    datos = InvoiceData(df)
    
    print(f'''
    Todas las propiedades de la clase InvoiceData son:
      
       
    La lista de revenue: 
      
    {datos.revenue}
      
    La lista de revenue por paises:
      
    {datos.revenue_countries}
      
    La lista de revenue por productos:
      
    {datos.revenue_products}
      
    La lista de revenue por dias:
      
    {datos.revenue_days}
      
    La lista de revenue por clientes:
    
    {datos.revenue_customer}
      
      
    ''')


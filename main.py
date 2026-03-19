import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns
import streamlit as st
from plot_dark_style import styles

from streamlit import session_state as SSTT
import time

from pandasAnylisis import InvoiceData , limpiar_df

@st.cache_data
def ReadCSV():
    return pd.read_csv('onret.zip' , parse_dates=['InvoiceDate'] , dtype={
            "Customer ID": "float32",
            "Quantity": "int32",
            "Price": "float32",
            "Country": "category",
        })
df = ReadCSV()
df = limpiar_df(df)
datos = InvoiceData(df)

# print(plt.rcParams.keys())

# agregamos las variables esenciales
if 'vars' not in SSTT : SSTT.vars = {
    'customer_control' : 'Top 10 customers',
    'revenue_control' : 'Revenue anual', # definimos los valores default
    'revenue_year_control' : 2011,
}

# styleamos con css

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1700px;   /* aumenta el ancho máximo */
        padding-left: 2rem;
        padding-right: 2rem;
        padding-top: 2.76rem;
        padding-bottom: 1rem;
    }
    header { 

    }
    </style>
    """,
    unsafe_allow_html=True
)

# parte grafica
sns.set_style('ticks')
plt.rcParams.update(styles)

col1Main , col2Main = st.columns([3,0.9])

# columna 1

with col1Main: 
    col1 , col2 = st.columns([1.4,2])
    with col1:
        # grafico de barras de customers y de pie
        with st.container(border = True , height= 310):
            @st.fragment
            def Customer():
                # selector de graficos
                # options = ['Top 10 customers' , 'Influencial revenue']
                # # selector
                #     SSTT.vars['customer_control'] = st.segmented_control(
                #         "Graficos Customer" , 
                #         options = options , 
                #         selection_mode= 'single',
                #         label_visibility = 'hidden',
                #         default = 'Top 10 customers',
                #     )
                tab1, tab2 = st.tabs(['Top 10 customers' , 'Influencial revenue'])
                with tab1:
                # grafico de top 10 customers
                # ----------------------------------------------------------
                #if SSTT.vars['customer_control'] == 'Top 10 customers':
                #------------------------------------------------------------
                    # grafico de barra
                    def CustomerBarras(): 
                        f , ax = plt.subplots(figsize = (9,5))
                        sns.barplot(
                            data = datos.revenue_customer,
                            x = 'Customer',
                            y = 'Total Revenue',
                            hue = 'Customer',
                            palette = 'rocket',
                            ax = ax,
                            legend = False,
                            linewidth = 0,
                        )
                        ax.spines[['left' , 'bottom']].set_linewidth(.8)
                        ax.spines[['left' , 'bottom']].set_color('white')
                        
                        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,pos : f'${x / 1000:.0f}K'))
                        ax.tick_params(axis = 'x' , which = 'major' , rotation = 28)
                        st.pyplot(f , width = 'stretch')   
                    CustomerBarras()
                    # grafico de influencia 
                # -----------------------------------------------------------------   
                #elif SSTT.vars['customer_control'] == 'Influencial revenue':
                # -----------------------------------------------------------------
                with tab2:
                    # calculamos el porcentaje de cada uno
                    def CustomerPie():
                        s = datos.df.groupby('Customer ID')['TotalPrice'].sum().sort_values(ascending=False)
                        sumaTotal = np.sum(s.values)
                        sumaCustomers = np.sum(datos.revenue_customer['Total Revenue'])
                        
                        f , ax  = plt.subplots(figsize = (9 , 3.8))
                        ax.pie(
                            x = [sumaTotal , sumaCustomers],
                            labels = [f'Total\n${sumaTotal:,.0f}' , f'Top 10 customers\n${sumaCustomers:,.0f}'],
                            radius = 1,
                            frame = False,
                            startangle= -30,
                            labeldistance= 1.25,
                            shadow = True,
                            wedgeprops = {'linewidth': 0},
                            colors = ["#261147" , "#3B2068"],
                            explode = [0.03 , 0.03]
                        )
                        
                        st.pyplot(f , width = 'stretch')
                    CustomerPie()
                
            Customer()
    with col2:
            
        with st.container(border = True , height = 310):
            @st.fragment
            def Revenue():
                # selector de graficos
                # options = ['Revenue anual' , 'Revenue anual detallado' , 'Revenue por dias de la semana']
                # # selector
                # SSTT.vars['revenue_control'] = st.segmented_control(
                #     "Graficos Revenue" , 
                #     options = options , 
                #     selection_mode= 'single',
                #     label_visibility = 'hidden',
                #     default = 'Revenue por dias de la semana',
                # )
                # grafico de barras de revenue anual
                tab1 , tab2 , tab3 = st.tabs(['Revenue anual' , 'Revenue anual detallado' , 'Revenue por dias de la semana'])
                # ---------------------------------------------------------------------
                # if SSTT.vars['revenue_control'] == 'Revenue anual':
                # ----------------------------------------------------------------------
                with tab1:
        
                    def RevenueLine():
                        f , ax = plt.subplots(figsize = (12 , 4.5))
                        
                        sns.lineplot(
                            data = datos.revenue,
                            x = 'Month',
                            y = 2011,
                            # hue = 'Month',
                            # palette = 'rocket',
                            color = "#8A3F13",
                            ax = ax,
                            legend = False,
                        )
                        ax.fill_between(datos.revenue["Month"], datos.revenue[SSTT.vars['revenue_year_control']], color="#8A3F13", alpha=0.2)
                        
                        ax.spines[['left' , 'bottom']].set_linewidth(.8)
                        ax.spines[['left' , 'bottom']].set_color('white')
                        ax.tick_params(axis = 'both' , which = 'major' , labelsize = 18)
                        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,pos : f'${x / 1000000:.1f}M'))
                        
                        st.pyplot(f , width = 'stretch' )  
                    RevenueLine()
                    
                
                # ahora este grafico es el heatmap con año y mes
                # -------------------------------------------------------------------
                # if SSTT.vars['revenue_control'] == 'Revenue anual detallado':
                # -------------------------------------------------------------------
                with tab2:
                    def RevenueMap():
                        f , ax = plt.subplots(figsize = (11 , 3.9))
                        
                        sns.heatmap(
                            data = datos.revenueTable,
                            cmap = 'rocket',
                            annot = True,
                            annot_kws= {'fontsize' : 14 },
                            ax = ax,
                            fmt = ",.0f",
                            cbar = False,
                            linewidths =2,
                            linecolor = "#0E1117", 
                        )
                        ax.tick_params(axis = 'both' , which = 'major' , labelsize = 16)
                        ax.xaxis.tick_top()
                        st.pyplot(f , width = 'stretch')
                    RevenueMap()
                
                # grafico de revenue por dias de la semana
                # -------------------------------------------------------------------
                # if SSTT.vars['revenue_control'] == 'Revenue por dias de la semana':
                # -------------------------------------------------------------------
                with tab3:
                    def RevenueDays():
                        s = datos.revenue_days.copy()
                        orden = ['Monday' , 'Tuesday' , 'Wednesday' , 'Thursday' , 'Friday' , 'Saturday' , 'Sunday']
                        s['Days'] = pd.Categorical(values = s['Days'] , categories= orden , ordered = False)
                        s = s.sort_values('Days')
                        
                        f , ax = plt.subplots(figsize = (11,4))
                        sns.lineplot(
                            data = s,
                            x = 'Days',
                            y = 'Revenue',
                            color = "#49369E",
                            ax = ax
                        )
                        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x , pos: f'${x / 1000000:.1f}M'))
                        ax.fill_between(s["Days"], s["Revenue"], color="#49369E", alpha=0.2)
                        ax.tick_params(axis = 'x' , which = 'major' , labelsize = 15)
                        print(f'\n\n el dataframe quedo asi: \n{s}\n\n')
                        
                        st.pyplot(f , width = 'stretch')
                    RevenueDays()
            Revenue()
    
    # parte de abajo de products
    with st.container(border = True):
        @st.fragment
        def ProductsBar():
            s = datos.revenue_products.copy()
            f , ax = plt.subplots(figsize = (18 , 3.3))
            norm = plt.Normalize(
                vmin = s['Mean Price'].min() -150, 
                vmax = s['Mean Price'].max() + 50, 
                clip = True
            )
            sns.barplot(
                data = s,
                x = 'Product',
                y = 'Total Revenue',
                hue = 'Mean Price',
                palette = 'rocket_r',
                hue_norm = norm,
                ax = ax,
                linewidth = 0,
            )
            ax.spines[['left' , 'bottom']].set_linewidth(.8)
            ax.spines[['left' , 'bottom']].set_color('white')
            
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,pos: f'${x / 1000:.0f}K'))
            ax.tick_params(axis = 'both' , which = 'major' , labelsize = 13)
            
            st.pyplot(f , width = 'content')
        ProductsBar()

# ahora vamos e escribir en la segunda columna (el sidebar de la derecha)
# -----------------------------------------------------------------------
with col2Main:
    @st.fragment
    def kpis():
        #-------------------------------
            #-----------metrics-------------
        s = datos.df.copy()
        c = s.groupby('Customer ID')['TotalPrice'].sum().sort_values(ascending=False)
        with st.container(border = True):
            htmlCarousel = f"""
            <div class="carousel">
                <div class="slide" style="font-size:16px; color:#888;">
                    Revenue in 2011 <br>
                    <p style="font-size:40px; color:#FFFFFF; font-weight:bold;">
                        ${np.sum(datos.revenue[2011]):,.0f}
                    </p>
                    <p style="font-size:20px; color:#FF0000; font-weight:bold; position:absolute; top:75px; right:45%;">
                        {(np.sum(datos.revenue[2011]) * 100) / np.sum(datos.revenue[2010]) - 100:.0f}%
                    </p>
                </div>
                <div class="slide" style="font-size:16px; color:#888;">
                    1st Country: {datos.revenue_countries['Countries'][0]} 
                    <p style="font-size:40px; color:#FFFFFF; font-weight:bold;">
                        ${datos.revenue_countries['Revenue'][0]:,.0f}
                    </p>
                </div>
                <div class="slide" style="font-size:16px; color:#888;">
                    Customers: <br>
                    <p style="font-size:40px; color:#FFFFFF; font-weight:bold;"> 
                        {c.shape[0]}
                    </p>
                </div>
                <div class="slide" style="font-size:16px; color:#888;">
                    Average Order Price: <br>
                    <p style="font-size:40px; color:#FFFFFF; font-weight:bold;">
                        ${np.mean(datos.df['TotalPrice']):,.1f}
                    </p>
                </div>
            </div>

            <style>
            .carousel {{
            display:flex;
            overflow:hidden;
            width:100%;
            height:110px;
            }}

            .slide {{
            min-width:100%;
            animation: slide 16s infinite;
            text-align:center;
            }}

            @keyframes slide {{
            0% {{transform: translateX(0)}}
            25% {{transform: translateX(-100%)}}
            50% {{transform: translateX(-200%)}}
            75% {{transform: translateX(-300%)}}
            }}
            </style>
            """
            st.markdown(htmlCarousel, unsafe_allow_html=True)         
    kpis()
    
    def CountriesPie():
        # ----------------------------------------------------------------
        # ---------------- pie de countries revenue -------------------------
        with st.container(border = True):
            f , ax = plt.subplots(figsize=(16,11))
            s = datos.revenue_countries
            total = np.sum(s['Revenue'])
            ax.pie(
                x = [s['Revenue'][0] , s['Revenue'][1] , s['Revenue'][2] , s['Revenue'][3] , s['Revenue'][4] , np.sum(s['Revenue'][4:])],
                labels = [
                    s['Countries'][0], 
                    s['Countries'][1],
                    s['Countries'][2], 
                    s['Countries'][3],   
                    s['Countries'][4], 
                    'Other Countries',   
                ],
                radius = 1.1,
                frame = False,
                startangle= 69,
                shadow = True,
                pctdistance=0.82,
                autopct='%1.0f%%',
                labeldistance=1.08,
                wedgeprops = {'linewidth': 0},
                colors = ["#261147" , "#3B2068"],
                textprops= {'fontsize' : 26},
                explode = [0.04,0.04,0.04,0.04,0.04,0.04],
            )
            st.pyplot(f , width = 'stretch')
    CountriesPie()
    
    # ----------------------------------------------------------------
    # --------------- tabla de countries -----------------------------
    
    st.dataframe(datos.revenue_countries , height = 195)

st.dataframe(datos.df)
     

        
    


            

    
   
    
    
    
            
        

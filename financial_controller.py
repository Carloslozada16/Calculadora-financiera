import matplotlib.pyplot as plt


def simular_credito( capital, interes, plazo_meses, valor_cuota, valor_seguro, abono_capital ) -> dict:
  
  lista_simulacion =[]
  n=1
  valor_cuota=valor_cuota + valor_seguro
  capital= capital
  b= valor_cuota + abono_capital
  while capital > 0 :
    p={}
    p.update({"mes":n})
    p.update({"saldo_inicial":capital})
    valor= calcular_nuevo_valor_adeudado(capital,interes)
    intereses = round(valor - capital,2)
    p.update({"intereses":intereses})    
    if valor+ valor_seguro < b and capital > 1 and (abono_capital > 0):
      abono_capital=valor+valor_seguro - valor_cuota  
      abono_capital= round(abono_capital,2)
      p.update({"abono_capital":abono_capital})     
      if abono_capital < 0:
        abono_capital= 0
        valor_cuota = valor + valor_seguro
        p.update({"abono_capital":abono_capital})  
        p.update({"total_cuota":valor_cuota}) 

    else:
       p.update({"abono_capital":abono_capital})  
    
    if valor + valor_seguro <= b and (valor + valor_seguro - b) <= 50 and abono_capital == 0:
      valor_cuota = valor + valor_seguro
      p.update({"total_cuota":valor_cuota}) 
    else:
      p.update({"total_cuota":valor_cuota})


    saldo_pago=valor + valor_seguro - valor_cuota - abono_capital
    saldo_pago=round(saldo_pago,2)
    p.update({"saldo_despues_pago":saldo_pago})

    #if n == 1:
    #  capital=capital
    #elif n >=1:
    #  capital= saldo_pago
    capital=saldo_pago           
    lista_simulacion.append(p)
    n += 1
  
  
  return lista_simulacion




def calcular_nuevo_valor_adeudado( capital, interes ) -> float:
  """
  la funcion retorna el valor de nuevo capital

  """
  tasames=convertir_interes_efectivo_anula_a_mensual(interes)
  intereses=capital * tasames
  capital= capital + intereses 

  # TODO: Desarrollar este método
  # AYUDA: usar el método "convertir_interes_efectivo_anula_a_mensual" para convertir el interes de anual a mensual"""
  return round(capital,2)




def convertir_interes_efectivo_anula_a_mensual(ea):
  """
    Convierte el interes de efectivo anula a efectivo mensual
  """
  return (1 + ea)**(1/12) - 1



def obtener_valor_cuota(monto, tasa, cuotas):
    """
    Retorna el valor actual de la cuota, para cuotas son fijas.
                
    Formula = R = P [(i (1 + i)**n) / ((1 + i)**n – 1)]. 
    Donde: 
        R = renta (cuota)
        P = principal (préstamo adquirido)
        i = tasa de interés
    """
    efectiva_mensual = convertir_interes_efectivo_anula_a_mensual(tasa)    
    valor_cuota = monto * ( (efectiva_mensual * ((1 + efectiva_mensual)**cuotas)) / (((1 + efectiva_mensual)**cuotas) - 1) )
    valor_cuota = valor_cuota + 1 # método para evitar un més adicional (truco)
    return round( valor_cuota, 2)


def graficar(capital, interes, plazo_meses, valor_cuota, valor_seguro, abono_capital):
  lista = simular_credito(capital, interes, plazo_meses, valor_cuota, valor_seguro, abono_capital)
  capital=[]
  interes=[]
  meses=[]
  for data in  lista:
   valor=float(data['total_cuota'])-(float(data['intereses']+float(valor_seguro)))  
   valor=round(valor,2)
   capital.append(valor)
   valor_interes=data['intereses']
   interes.append(valor_interes)
   mes=data['mes']
   meses.append(mes)  
  plt.bar(meses, capital, label='Capital')
  plt.bar(meses, interes, label='interes',  bottom=capital)
   #plt.hist(x=meses,bins=capital)
   #plt.title('Histograma Capital - intereses')
   #plt.xlabel('Meses')
   # plt.ylabel('Frecuencia')
  
  plt.show()   
  


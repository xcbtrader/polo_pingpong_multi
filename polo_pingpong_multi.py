__author__ = 'xcbtrader'
# -*- coding: utf-8 -*-

import poloniex
import time
import sys

def leer_ticker(c):
	global polo

	err = True
	while err:
		try:		
			ticker = polo.returnTicker()
			c = 'USDT_' + c
			t = ticker[c]
			last = float(t['last'])
			return last
		except KeyboardInterrupt:
			exit()	
		except Exception:
			print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
			print('### ERROR AL LEER PRECIO BTC_USDT ###')
			print('### ESPERANDO 30 SEGUNDOS ###')
			time.sleep(30)		

def leer_balance(c):
	global polo

	err = True
	while err:
		try:
			balance = polo.returnBalances()
			return float(balance['USDT']), float(balance[c])
		except KeyboardInterrupt:
			exit()	
		except Exception:
			print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
			print('### ERROR AL LEER SALDOS DE LA CUENTA ###')
			print('### ESPERANDO 30 SEGUNDOS ###')
			time.sleep(30)
			
def realizar_compra(n_coin, c, last, margen, saldo_inv):
	global polo, tot_buy

	precio_compra = last - (last * margen)
	c = 'USDT_' + c

	err = True
	while err:	
		try:
			make_order_buy = polo.buy(c,precio_compra,saldo_inv/precio_compra)
			tot_buy[n_coin] +=1
			guardar_ordenes('CREADA ORDEN COMPRA', c, make_order_buy['orderNumber'], str(precio_compra), str(saldo_inv))
			print('*****************************************************************************')
			print('*** CREADA ORDEN DE COMPRA NUM ' + make_order_buy['orderNumber'] + ' - PRECIO: ' + str(precio_compra) + ' $ - IVERSION: ' + str(saldo_inv) + ' ' + c + ' ***')
			print('*****************************************************************************')
			err = False
			time.sleep(15)
		except KeyboardInterrupt:
			exit()	
		except Exception:
			print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
			print('### ERROR AL CREAR ORDEN DE COMPRA ###')
			print('### ESPERANDO 30 SEGUNDOS ###')
			time.sleep(30)	
	
def realizar_venta(n_coin, c, last, margen, saldo_inv):
	global polo, tot_sell
	
	precio_venta = last + (last * margen)
	c = 'USDT_' + c
	
	err = True
	while err:	
		try:
			make_order_sell = polo.sell(c, precio_venta, saldo_inv)
			tot_sell[n_coin] +=1
			guardar_ordenes('CREADA ORDEN VENTA', c, make_order_sell['orderNumber'], str(precio_venta), str(saldo_inv))
			print('*****************************************************************************')
			print('*** CREADA ORDEN DE VENTA NUM ' + make_order_sell['orderNumber'] + ' - PRECIO: ' + str(precio_venta) + ' $ - IVERSION: ' + str(saldo_inv) +  ' $ ***')
			print('*****************************************************************************')
			err = False
			time.sleep(15)
		except KeyboardInterrupt:
			exit()	
		except Exception:
			print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
			print('### ERROR AL CREAR ORDEN DE VENTA ###')
			print('### ESPERANDO 30 SEGUNDOS ###')
			time.sleep(30)

def guardar_ordenes(cabecera, c, t1, t2, t3):
	fecha = str(time.strftime("%d/%m/%y")) + ' ' + str(time.strftime("%H:%M:%S"))
	fOrdenes = open('polo_pingpong_multi_ordenes.txt', 'a')
	fOrdenes.write(cabecera + ';' + fecha + ';USD_' + c + ';'+ t1 + ';' + t2 + ';' + t3 + '\n')
	fOrdenes.close()
	
def leer_ordenes(c):
	global polo
	
	c = 'USDT_' + c
	err = True
	while err:
		try:
			openOrders = polo.returnOpenOrders(c)
			return openOrders
		except KeyboardInterrupt:
			exit()	
		except Exception:
			print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
			print('### ERROR AL LEER LAS ORDENES ABIERTAS ###')
			print('### ESPERANDO 30 SEGUNDOS ###')
			time.sleep(30)

# PROGRAMA PRINCIPAL #####################################################################

global tot_buy, tot_sell, polo, coins

print('')
print('**************************************************************')
print('         INICIANDO BOT POLONIEX PingPong MULTI COIN')
print('**************************************************************')
print('')

API_key = 'PONER AQUI NUESTRA API_KEY'
Secret = 'PONER AQUI NUESTRO SECRET'

err = True
while err:
	try:
		polo = poloniex.Poloniex(API_key,Secret)
		err = False
		print('### CONECTADO CORRECTAMENTE A LA API DE POLONIEX ###')
		print('')
	except KeyboardInterrupt:
		exit()
	except Exception:
		print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
		print('### ERROR AL CONECTAR CON API POLONEX ###')
		print('### ESPERANDO 30 SEGUNDOS ###')
		time.sleep(30)



coins = ['BTC', 'LTC', 'ETH', 'DASH', 'XRP', 'ETC', 'XMR']

porcentaje_inv = 0.0
while porcentaje_inv <5:
	m = str(input('Entra margen de beneficio BTC(>=5) :? '))
	porcentaje_inv = float(m.replace(',','.'))

porcentaje_inv = porcentaje_inv/100

margenBTC = 0.0
while margenBTC <0.15:
	m = str(input('Entra margen de beneficio BTC(>=0.15) :? '))
	margenBTC = float(m.replace(',','.'))

margenBTC = margenBTC/100

margenALT = 0.0
while margenALT <0.15:
	m = str(input('Entra margen de beneficio ALTCOINS(>=0.15) :? '))
	margenALT = float(m.replace(',','.'))

margenALT = margenALT/100

tot_buy = []
tot_sell = []
saldos = []
saldos_inv = []
tipo_orden = []

for c in coins:
	saldos.append(0.0)
	saldos_inv.append(0.0)
	tot_buy.append(0)
	tot_sell.append(0)
	tipo_orden.append('sell')

saldoUSDTinv = 0.0

saldoUSDT, s = leer_balance('BTC')

saldoUSDTinv = ((saldoUSDT * porcentaje_inv)/len(coins)) * 0.98
n = 1

while True:
	n_coin = 0
	for c in coins:
		openOrders = leer_ordenes(c)
		nOrdenes = len(openOrders)

		if n_coin == 0:
			margen = margenBTC
		else:
			margen = margenALT

		if nOrdenes == 0:
			saldoUSDT, saldos[n_coin] = leer_balance(c)
			last = leer_ticker(c)
								
			if tipo_orden[n_coin] == 'sell': #SITUACON DE COMPRA
				tipo_orden[n_coin] = 'buy'
				
				realizar_compra(n_coin, c, last, margen, saldoUSDTinv)
			else: # SITUACION DE VENTA
				saldo_inv = saldos[n_coin] * 0.98
				tipo_orden[n_coin] = 'sell'
				realizar_venta(n_coin, c, last, margen,saldo_inv)

		elif nOrdenes == 1: # Escenario con toda la inversion aun abierta. No hacer nada
			last = leer_ticker(c)
			
			print('-------------------------------------------------------')
			print('MARGEN: ' + str(margen * 100) + ' % --  PAR: USDT_' + c)
			print(str(n) + ') Buy Ord: ' + str(tot_buy[n_coin]) + ' - Sell Ord: ' + str(tot_sell[n_coin]) + ' - ' + c + ' = ' + str(last) + ' $')
			for orde in openOrders:
				print(orde['type'] + ' - ' + orde['date'] + ' - ' + orde['rate'] + ' $ - ' + orde['amount'] + ' ' + c)
			print('-------------------------------------------------------')
			print('### ESPERANDO 30 SEGUNDOS PARA CONTINUAR ###')
			time.sleep(30)
		n +=1
		n_coin +=1

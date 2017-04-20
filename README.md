# polo_pingpong_multi
Poloniex, Bot para autotrader Multi Altcoin

Poloniex, Bot para autotrader en Multi Altcoin, divide nuestra inversión en 7 Alcoins ('BTC', 'LTC', 'ETH', 'DASH', 'XRP', 'ETC', 'XMR') Este Bot está preparado para trabajar en Python 2.7. No funciona en Python 3.6 o superior Utilizarlo bajo vuestra responsabilidad !!!!

No me hago responsable de posibles fallos, pérdidas o operaciones incorrectas que pueda realizar el Bot

Para instalarlo, antes hay que instalarse las librerias de Poloniex del siguiente link:

https://github.com/s4w3d0ff/python-poloniex

Antes de ejecutar el programa, hay que editarlo y modificar la línea donde se pide los datos del API. Si no los tenemos creados, antes hay que ir a la web de Poloniex y crear una llave de API.

Para ejecutarlo poner:

python polo_pingpong_multi.py

Una vez ejecutado, nos pedirá el márgen de beneficio que queremos en cada operación, tanto para el par USDT_BTC como para las demas AltCoins. Cuanto más grande sea, tardará más en cerrar las operaciones, pero más beneficio tendremos. El bot funcionrá mientras tengamos saldo. Para su correcto funcionamiento, necesitamos tener saldo de USDT, y ninguna operacion abierta en el par USDT_BTC ni las otras AltCoins.

Evidentemente, para que el bot funcione, se necesita tenerlo siempre funcionando y una conexión a internet. Los datos los consulta cada 10 minutos, por lo que no consume ancho de banda.

El funcionamiento del bot es sencillo:

Al iniciarlo, comprueba que no haya operaciones abiertas, y mira nuestro saldo USDT. La cantidad que se utilizará en cada orden, se calcula con la siguiente fórmula: saldo_inicial_USDT/número de AltCoins del bot(7).

Entonces el sistema pone una órden de compra de cada AltCoin, al precio del mercado - margen. Una vez cerrada esta órdn, el bot hace el proceso contrario, pone una órden de venta al precio del mercado + margen de beneficio, y así continuamente para cada AltCoin por separado.

Para finalizar el proceso, simplemente apretar CTRL + c.

Si el bot nos deja órdenes abiertas, y las queremos cerrar, simplemente, vamos a POLONIEX, y las cerramos.

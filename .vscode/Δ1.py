import asyncio
import aiohttp
import logging
import time

"""
pybotters が対応してる各取引所の WebSocket エンドポイントに `heartbeat = 10.0` で接続するテストコード。
何も購読せず、切断時に接続時間を表示する。
"""

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

heartbeat = 10.0

async def ws_session(session: aiohttp.ClientSession, url: str):
    timer = None
    try:
        async with session.ws_connect(url, heartbeat=heartbeat) as ws:
            timer = time.time()
            logger.info({"event": "open", "url": url})
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.ERROR:
                    logger.error(msg)
                    break
                else:
                    logger.info({"event": "message", "url": url, "data": msg.data})
    except Exception as e:
        logger.error({"event": "error", "url": url, "error": f"{e.__class__.__name__}: {e}"})
    finally:
        if timer:
            logger.info({"event": "close", "url": url, "time": f"{time.time() - timer:.3f}"})
        else:
            logger.info({"event": "close", "url": url})

async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            # echo demo server
            # ws_session(session, "ws://echo.websocket.events"),
            # ws_session(session, "ws://echo.websocket.org"),
            # Bybit
            ws_session(session, "wss://stream.bybit.com/realtime"),
            ws_session(session, "wss://stream.bybit.com/realtime_public"),
            ws_session(session, "wss://stream.bybit.com/realtime_private"),
            ws_session(session, "wss://stream.bybit.com/spot/quote/ws/v1"),
            ws_session(session, "wss://stream.bybit.com/spot/quote/ws/v2"),
            ws_session(session, "wss://stream.bybit.com/spot/ws"),
            ws_session(session, "wss://stream.bybit.com/perpetual/ws/v1/realtime_public"),
            ws_session(session, "wss://stream.bybit.com/trade/option/usdc/private/v1"),
            # Binance
            ws_session(session, "wss://stream.binance.com:9443/stream"),
            ws_session(session, "wss://nbstream.binance.com/lvt-p/stream"),
            ws_session(session, "wss://fstream.binance.com/stream"),
            # ws_session(session, "wss://fstream-auth.binance.com/stream"),
            ws_session(session, "wss://dstream.binance.com/stream"),
            ws_session(session, "wss://vstream.binance.com/stream"),
            # OKX
            ws_session(session, "wss://ws.okx.com:8443/ws/v5/public"),
            ws_session(session, "wss://ws.okx.com:8443/ws/v5/private"),
            # Phemex
            ws_session(session, "wss://phemex.com/ws"),
            # Bitget
            ws_session(session, "wss://ws.bitget.com/spot/v1/stream"),
            ws_session(session, "wss://ws.bitget.com/mix/v1/stream"),
            # MEXC
            ws_session(session, "wss://contract.mexc.com/ws"),
            # FTX
            ws_session(session, "wss://ftx.com/ws/"),
            # BitMEX
            ws_session(session, "wss://ws.bitmex.com/realtime"),
            # bitFlyer
            ws_session(session, "wss://io.lightstream.bitflyer.com/socket.io/?EIO=3&transport=websocket"),
            ws_session(session, "wss://ws.lightstream.bitflyer.com/json-rpc"),
            # GMO Coin
            ws_session(session, "wss://api.coin.z.com/ws/public/v1"),
            # ws_session(session, "wss://api.coin.z.com/ws/private/v1"),
            # Liquid
            ws_session(session, "wss://tap.liquid.com/app/LiquidTapClient"),
            # bitbank
            ws_session(session, "wss://stream.bitbank.cc/socket.io/?EIO=3&transport=websocket"),
            # Coincheck
            ws_session(session, "wss://ws-api.coincheck.com/"),
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

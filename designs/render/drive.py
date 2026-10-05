"""Renders a list of jobs with render.html in headless Chromium.
Usage: python3 drive.py jobs.json [port]   (repo root must be served on port)"""
import asyncio, base64, io, json, sys
from playwright.async_api import async_playwright
from PIL import Image

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"


async def main(jobs, port):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME, args=[
            "--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        pg = await b.new_page()
        pg.on("pageerror", lambda e: print("pageerror:", e))
        await pg.goto(f"http://127.0.0.1:{port}/designs/render/render.html")
        await pg.wait_for_function("window.ready===true")
        for j in jobs:
            url = await pg.evaluate("o => window.renderView(o)", j["opts"])
            Image.open(io.BytesIO(base64.b64decode(url.split(",")[1]))).save(j["out"])
        await b.close()


if __name__ == "__main__":
    asyncio.run(main(json.load(open(sys.argv[1])), int(sys.argv[2]) if len(sys.argv) > 2 else 8790))

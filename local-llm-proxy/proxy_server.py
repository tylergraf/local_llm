#!/usr/bin/env python3
"""
Local LLM Proxy Server
Forwards requests to external LLM server configured in add-on options
"""

import os
import sys
import asyncio
import logging
from aiohttp import web, ClientSession, ClientTimeout

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration from environment (set by run.sh from add-on config)
LLM_SERVER_URL = os.getenv('LLM_SERVER_URL', 'http://localhost:11434').rstrip('/')
API_KEY = os.getenv('API_KEY', '')
TIMEOUT = int(os.getenv('TIMEOUT', '120'))

logger.info(f"Proxy will forward to: {LLM_SERVER_URL}")
logger.info(f"Request timeout: {TIMEOUT}s")


async def proxy_handler(request):
    """
    Proxy all requests to the configured LLM server
    """
    # Get the path (everything after the initial /)
    path = request.match_info.get('path', '')
    
    # Build target URL
    target_url = f"{LLM_SERVER_URL}/{path}"
    
    # Copy headers, add API key if provided
    headers = dict(request.headers)
    # Remove hop-by-hop headers
    headers.pop('Host', None)
    headers.pop('Connection', None)
    
    if API_KEY:
        headers['Authorization'] = f'Bearer {API_KEY}'
    
    logger.debug(f"Proxying {request.method} {path} -> {target_url}")
    
    try:
        async with ClientSession(timeout=ClientTimeout(total=TIMEOUT)) as session:
            # Read request body
            body = await request.read()
            
            # Forward request to LLM server
            async with session.request(
                method=request.method,
                url=target_url,
                headers=headers,
                params=request.query,
                data=body
            ) as response:
                # Read response
                response_body = await response.read()
                
                # Copy response headers
                response_headers = dict(response.headers)
                # Remove hop-by-hop headers
                response_headers.pop('Transfer-Encoding', None)
                response_headers.pop('Connection', None)
                
                # Return proxied response
                return web.Response(
                    body=response_body,
                    status=response.status,
                    headers=response_headers
                )
                
    except asyncio.TimeoutError:
        logger.error(f"Timeout connecting to {target_url}")
        return web.json_response(
            {'error': 'Timeout connecting to LLM server'},
            status=504
        )
    except Exception as e:
        logger.error(f"Error proxying request: {e}")
        return web.json_response(
            {'error': f'Error connecting to LLM server: {str(e)}'},
            status=502
        )


async def health_check(request):
    """Health check endpoint"""
    return web.json_response({
        'status': 'healthy',
        'target': LLM_SERVER_URL
    })


async def init_app():
    """Initialize the web application"""
    app = web.Application()
    
    # Health check
    app.router.add_get('/health', health_check)
    
    # Proxy all other requests
    app.router.add_route('*', '/{path:.*}', proxy_handler)
    
    return app


def main():
    """Main entry point"""
    logger.info("Starting Local LLM Proxy Server")
    logger.info(f"Forwarding to: {LLM_SERVER_URL}")
    
    app = asyncio.run(init_app())
    
    web.run_app(
        app,
        host='0.0.0.0',
        port=8080,
        access_log=logger
    )


if __name__ == '__main__':
    main()

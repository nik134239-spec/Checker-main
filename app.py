@app.route("/shopify", methods=["GET"])
def shopify_check():
    """
    Main checker endpoint — matches your bot's expected format
    GET /shopify?cc=4111|12|2026|123&site=example.com&proxy=ip:port:user:pass
    """
    start_time = time.time()
    
    # Get parameters
    cc_raw = request.args.get("cc", "").strip()
    site = request.args.get("site", "").strip()
    proxy = request.args.get("proxy", "").strip()
    
    # Validate inputs
    if not cc_raw:
        return jsonify({
            "error": "Missing 'cc' parameter",
            "format": "cc=4111111111111111|12|2026|123",
            "status": False
        }), 400
    
    if not site:
        return jsonify({
            "error": "Missing 'site' parameter",
            "format": "site=example.myshopify.com",
            "status": False
        }), 400
    
    # Parse card
    try:
        parts = parse_cc_string(cc_raw)
        cc = parts["cc"]
        mes = parts["mes"]
        ano = parts["ano"]
        cvv = parts["cvv"]
    except Exception as e:
        return jsonify({
            "error": f"Invalid CC format: {str(e)}",
            "format": "CC|MM|YYYY|CVV",
            "status": False
        }), 400
    
    # Process card asynchronously
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                process_card(cc, mes, ano, cvv, site, proxy_str=proxy or None)
            )
            
            # Check if result is None or invalid
            if result is None:
                return jsonify({
                    "error": "Checker returned no result. Site may not be Shopify or proxy is dead.",
                    "cc": cc_raw,
                    "site": site,
                    "proxy": proxy or "None",
                    "status": False,
                    "response": "CHECKER_FAILED",
                    "gateway": "Unknown",
                    "price": "0.00",
                    "currency": "USD",
                    "time": f"{round(time.time() - start_time, 2)}s"
                }), 200
            
            # Unpack result
            success, message, gateway, total_price, currency = result
            
        except Exception as e:
            return jsonify({
                "error": str(e),
                "cc": cc_raw,
                "site": site,
                "proxy": proxy or "None",
                "status": False,
                "response": "EXCEPTION",
                "gateway": "Unknown",
                "price": "0.00",
                "currency": "USD",
                "time": f"{round(time.time() - start_time, 2)}s"
            }), 200
        finally:
            loop.close()
            
    except Exception as e:
        return jsonify({
            "error": f"Loop error: {str(e)}",
            "status": False,
            "cc": cc_raw,
            "site": site
        }), 500
    
    elapsed = round(time.time() - start_time, 2)
    clean_msg = extract_clean_response(message) if message else "UNKNOWN"
    
    # Build response
    response_data = {
        "cc": cc_raw,
        "site": site,
        "proxy": proxy or "None",
        "status": success if success is not None else False,
        "response": clean_msg,
        "gateway": gateway if gateway else "Unknown",
        "price": total_price if total_price else "0.00",
        "currency": currency if currency else "USD",
        "time": f"{elapsed}s"
    }
    
    return jsonify(response_data)
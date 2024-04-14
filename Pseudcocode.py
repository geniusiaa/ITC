def Automatic_Order(item_id, current_date):
    # Step 1: Gather data
    sales_data = get_historical_sales(item_id)
    lead_time = get_lead_time(item_id)
    item_cost = get_item_cost(item_id)

    # Step 2: ABC Analysis
    a_items, b_items, c_items = perform_abc_analysis(sales_data, item_cost)

    if item_id in a_items or item_id in b_items:
        # Step 3: Calculate Safety Stock
        demand_mean = calculate_demand_mean(sales_data)
        demand_variance = calculate_demand_variance(sales_data)
        lead_time_mean = calculate_lead_time_mean(lead_time)
        lead_time_variance = calculate_lead_time_variance(lead_time)
        service_level = get_desired_service_level(item_id)

        safety_stock = calculate_safety_stock(demand_mean, demand_variance, lead_time_mean, lead_time_variance, service_level)

        # Step 4: Calculate Reorder Point
        forecasted_demand = forecast_demand(sales_data, lead_time, current_date)
        reorder_point = calculate_reorder_point(forecasted_demand, safety_stock)
    else:
        # Step 5: Tracking Inventory Level
        on_hand = get_inventory_on_hand(item_id)
        pipeline = get_pipeline_inventory(item_id)
        backlog = get_backlog_inventory(item_id)
        available_inventory = on_hand + pipeline - backlog

        # Step 6: Check if current level is below ROP
        if available_inventory < reorder_point:
            # Step 7: Get Minimum Order Quantity (MOQ) from supplier
            standard_moq = get_supplier_moq(item_id)

            # Step 8: Calculate EOQ and MOQ Standard
            eoq = calculate_eoq(sales_data, item_cost)
            moq_standard = calculate_moq_standard(standard_moq, sales_data, lead_time, item_cost)
            order_quantity = max(eoq, moq_standard)

            # Step 9: Place Order
            place_order(item_id, order_quantity)

    # Step 5: Tracking Inventory Level (for A and B items)
    on_hand = get_inventory_on_hand(item_id)
    pipeline = get_pipeline_inventory(item_id)
    backlog = get_backlog_inventory(item_id)
    available_inventory = on_hand + pipeline - backlog

    # Step 6: Check if current level is below ROP (for A and B items)
    if available_inventory < reorder_point:
        # Step 7: Get Minimum Order Quantity (MOQ) from supplier
        standard_moq = get_supplier_moq(item_id)

        # Step 8: Calculate EOQ and MOQ Standard
        eoq = calculate_eoq(sales_data, item_cost)
        moq_standard = calculate_moq_standard(standard_moq, sales_data, lead_time, item_cost)
        order_quantity = max(eoq, moq_standard)

        # Step 9: Place Order
        place_order(item_id, order_quantity)

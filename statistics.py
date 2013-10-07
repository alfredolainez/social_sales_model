import model
import numpy
import math

def get_statistics(graph, reward_model, initial_sale_price):

    client_sales = model.get_sales_per_client(graph, reward_model)
    total_earned = 0
    users_reductions = []
    for sale in client_sales:
        first_grade_reduction = initial_sale_price * reward_model.discounts[0] * sale[0]
        second_grade_reduction = initial_sale_price * reward_model.discounts[1] * sale[1]
        user_original_reduction = (first_grade_reduction, second_grade_reduction)

        if reward_model.limited:
            if len(reward_model.discount_limits) > 0:
                if first_grade_reduction > initial_sale_price * reward_model.discount_limits[0]:
                    first_grade_reduction = initial_sale_price * reward_model.discount_limits[0]
                if second_grade_reduction > initial_sale_price * reward_model.discount_limits[1]:
                    second_grade_reduction = initial_sale_price * reward_model.discount_limits[1]
            if first_grade_reduction + second_grade_reduction > initial_sale_price * reward_model.total_discount_limit:
                first_grade_reduction = initial_sale_price * reward_model.total_discount_limit
                second_grade_reduction = 0

        user_final_reduction = (first_grade_reduction, second_grade_reduction)
        total_earned += initial_sale_price - first_grade_reduction - second_grade_reduction
        users_reductions.append((user_original_reduction, user_final_reduction))

    return (total_earned, users_reductions)



def get_statistics_vs_coop(coop_samples, stock, market_price, initial_sale_price, reward_model):

    print "Total stock market price: " + str(stock * market_price)
    print "Initial stock value price: " + str(stock * initial_sale_price)

    cooperations = []
    earnings = []
    users_reductions_per_coop = []

    for i in range(0, coop_samples + 1):
        cooperation = i * float(1)/coop_samples
        g = model.generateRandomGraph(cooperation, stock, reward_model)
        total_earned, users_reductions = get_statistics(g, reward_model, initial_sale_price)

        print "Cooperation: " + str(cooperation) + " => " + str(total_earned)
        cooperations.append(cooperation)
        earnings.append(total_earned)
        users_reductions_per_coop.append(users_reductions)

    return (cooperations, earnings, users_reductions_per_coop)


def get_stats_original_discount(users_reductions):
    # Sum first and second grade discounts
    original_reductions = [reductions[0][0] + reductions[0][1] for reductions in users_reductions]
    return {'mean': numpy.mean(original_reductions),
            'sd': numpy.std(original_reductions)}

def get_benefits_vs_numsales(sales_samples, stock, model, initial_price, market_price_zones):

    def get_market_price_for_sales(num_sales, market_price_zones):
        """
        Gets market price for a number of sales given intervals of sales and their
        corresponding market prices
        """

        for (sales_interval, market_price) in market_price_zones:
            if sales_interval[0] <= num_sales <= sales_interval[1]:
                return market_price
        return 0


    sales_list = []
    worst_case_results = []
    best_case_results = []
    for i in range(0, sales_samples + 1):
        num_sales = math.floor(i * float(stock)/sales_samples)
        market_price = get_market_price_for_sales(num_sales, market_price_zones)
        cost = market_price * num_sales
        best_case = num_sales * initial_price - cost
        worst_case = num_sales * initial_price - cost - model.maximum_discount(num_sales, initial_price)

        sales_list.append(num_sales)
        worst_case_results.append(worst_case)
        best_case_results.append(best_case)

    return (sales_list, worst_case_results, best_case_results)
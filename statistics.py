import model
import numpy

def get_statistics(graph, reward_model, initial_sale_prize):

    client_sales = model.getSalesPerClient(graph, reward_model)
    total_earned = 0
    users_reductions = []
    for sale in client_sales:
        first_grade_reduction = initial_sale_prize * reward_model.discounts[0] * sale[0]
        second_grade_reduction = initial_sale_prize * reward_model.discounts[1] * sale[1]
        user_original_reduction = (first_grade_reduction, second_grade_reduction)

        if reward_model.limited:
            if len(reward_model.discount_limits) > 0:
                if first_grade_reduction > initial_sale_prize * reward_model.discount_limits[0]:
                    first_grade_reduction = initial_sale_prize * reward_model.discount_limits[0]
                if second_grade_reduction > initial_sale_prize * reward_model.discount_limits[1]:
                    second_grade_reduction = initial_sale_prize * reward_model.discount_limits[1]
            if first_grade_reduction + second_grade_reduction > initial_sale_prize * reward_model.total_discount_limit:
                first_grade_reduction = initial_sale_prize * reward_model.total_discount_limit
                second_grade_reduction = 0

        user_final_reduction = (first_grade_reduction, second_grade_reduction)
        total_earned += initial_sale_prize - first_grade_reduction - second_grade_reduction
        users_reductions.append((user_original_reduction, user_final_reduction))

    return (total_earned, users_reductions)



def get_statistics_vs_coop(coop_samples, stock, market_price, initial_sale_price, reward_model):

    print "Total stock market_prize: " + str(stock * market_price)
    print "Initial stock value prize: " + str(stock * initial_sale_price)

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



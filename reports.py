# -*- coding: utf-8 -*-
import model
import statistics as stats
from model import RewardModel
from matplotlib import pyplot as plot
from matplotlib.backends.backend_pdf import PdfPages


def plot_clients_discount(cooperation, stock, reward_model, initial_sale_price):
    g = model.generateRandomGraph(cooperation, stock, reward_model)
    total_earned, users_reductions = stats.get_statistics(g, reward_model, initial_sale_price)
    original_reductions = [(reductions[0][0] + reductions[0][1])/initial_sale_price * 100 for reductions in users_reductions]
    plot.title(u"coord index = " + str(cooperation))
    plot.xlabel(u"Descuento en %")
    plot.ylabel(u"Número de clientes")
    plot.hist(original_reductions, 40)

    return

def plot_clients_discount_histograms(stock, reward_model, initial_sale_price, show_plot=True):
    grid_size = (2, 2)

    plot.subplot2grid(grid_size, (0,0))
    plot_clients_discount(0.4, stock, reward_model, initial_sale_price)

    plot.subplot2grid(grid_size, (0,1))
    plot_clients_discount(0.6, stock, reward_model, initial_sale_price)

    plot.subplot2grid(grid_size, (1,0))
    plot_clients_discount(0.8, stock, reward_model, initial_sale_price)

    plot.subplot2grid(grid_size, (1,1))
    plot_clients_discount(1, stock, reward_model, initial_sale_price)

    plot.tight_layout()

    if show_plot:
        plot.show()

def plot_average_vs_coop(cooperations, averages, sds, show_plot=True):
    plot.plot(cooperations, averages, label="Mean")
    plot.plot(cooperations, sds, label="Standard deviation")
    plot.xlabel(u'índice de cooperación')
    plot.ylabel(u'descuento medio de precio en %')
    plot.title(u'Descuento medio según cooperación')
    plot.legend(loc='best')
    if show_plot:
        plot.show()

def plot_sales_vs_coop(cooperations, earnings, earnings_mutual_benefit, total_spent=None, constant_sale=None, show_plot=True):
    plot.plot(cooperations, earnings, label="Incentivo solo vendedor")
    plot.plot(cooperations, earnings_mutual_benefit, linestyle='--', color='k', label="Incentivo mutuo")
    if total_spent != None:
        plot.plot(cooperations, [total_spent]*len(cooperations), color='r', label="Gasto total")
    if constant_sale != None:
        plot.plot(cooperations, [constant_sale]*len(cooperations), color='g', label="Venta directa")

    plot.xlabel(u'índice de cooperación')
    plot.ylabel(u'total obtenido')
    plot.title(u'Ventas brutas vs cooperación')
    if total_spent == None:
        minimum = min(earnings + earnings_mutual_benefit)
    else:
        minimum = total_spent
    plot.ylim(minimum * 0.9, max(earnings) * 1.1)
    plot.legend(loc='best')

    if show_plot:
        plot.show()


def generate_report(cooperation_samples, stock, market_price, initial_price, discounts):

    pdf_pages = PdfPages('superdocumento.pdf')

    model1 = RewardModel(discounts, mutual_benefit=False)
    (cooperations, earnings, users_reductions) = stats.get_statistics_vs_coop(cooperation_samples, stock,
                                                                           market_price, initial_price, model1)
    model2 = RewardModel(discounts, mutual_benefit=True)
    (cooperations, earnings_mutual_benefit, users_reductions) = \
        stats.get_statistics_vs_coop(cooperation_samples, stock, market_price, initial_price, model2)

    plot_sales_vs_coop(cooperations, earnings, earnings_mutual_benefit, total_spent=stock * market_price, show_plot=False)
    pdf_pages.savefig()

    plot.figure()
    average_original_reductions = [stats.get_stats_original_discount(x)['mean']/float(initial_price) * 100 for x in users_reductions]
    sd_original_reductions = [stats.get_stats_original_discount(x)['sd']/float(initial_price) * 100 for x in users_reductions]

    plot_average_vs_coop(cooperations, average_original_reductions, sd_original_reductions, show_plot=False)
    pdf_pages.savefig()

    plot.figure()
    plot_clients_discount_histograms(NUMBER_PRODUCTS, model1, INITIAL_PRICE, show_plot=False)
    pdf_pages.savefig()

    plot.figure()
    plot_clients_discount_histograms(NUMBER_PRODUCTS, model2, INITIAL_PRICE, show_plot=False)
    pdf_pages.savefig()

    pdf_pages.close()




if __name__ == "__main__":
    COOPERATION_SAMPLES = 100
    NUMBER_PRODUCTS = 10000
    MARKET_PRICE = 225
    INITIAL_PRICE = 375

    DISCOUNTS = [0.03, 0.01]

    generate_report(COOPERATION_SAMPLES, NUMBER_PRODUCTS, MARKET_PRICE, INITIAL_PRICE, DISCOUNTS)

    #
    #
    # model1 = RewardModel(DISCOUNTS, mutual_benefit=False)
    # (cooperations, earnings, users_reductions) = getStatisticsVsCoop(COOPERATION_SAMPLES, NUMBER_PRODUCTS, MARKET_PRICE, INITIAL_PRICE, model1)
    # model2 = RewardModel(DISCOUNTS, mutual_benefit=True)
    # (cooperations, earnings_mutual_benefit, users_reductions) = getStatisticsVsCoop(COOPERATION_SAMPLES, NUMBER_PRODUCTS, MARKET_PRICE, INITIAL_PRICE, model2)
    #
    # plot_sales_vs_coop(cooperations, earnings, earnings_mutual_benefit)# 700000, 900000)
    #
    # average_original_reductions = [get_stats_original_discount(x)['mean']/float(INITIAL_PRICE) * 100 for x in users_reductions]
    # sd_original_reductions = [get_stats_original_discount(x)['sd']/float(INITIAL_PRICE) * 100 for x in users_reductions]
    #
    # plot_average_vs_coop(cooperations, average_original_reductions, sd_original_reductions)
    #
    # plotClientsDiscountHistograms(NUMBER_PRODUCTS, model1, INITIAL_PRICE)
    # plotClientsDiscountHistograms(NUMBER_PRODUCTS, model2, INITIAL_PRICE)

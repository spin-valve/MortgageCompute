import math
from typing import Any

class Mortgage:
    def __init__(self, mortgage, month, interest_rate):
        # 贷款总额
        self.mortgage = mortgage
        # 贷款时间
        self.month = month
        # 贷款年利率
        self.interest_rate = interest_rate
        # 月利率
        self.interest_rate_permonth = interest_rate / 12
        # 利息总和
        self.total_interest = 0.0
        # 本息和
        self.total_payment = 0.0

    # 等额本金
    def equal_principal(self):
        principal = self.mortgage / self.month
        # 每月还款结果
        repayment_arr = []
        for i in range(self.month):
            rest_total = self.mortgage - i * principal
            rest_interest = rest_total * self.interest_rate_permonth
            repayment = principal + rest_interest
            repayment_arr.append(round(repayment, 2))
        total_m = sum(repayment_arr)
        print("还款总额:%0.2f" % total_m)
        print("支付总利息:%0.2f" % (total_m - self.mortgage))
        print("首月还款:%0.2f" % repayment_arr[0])
        print("每月还款递减:%0.2f" % (principal * self.interest_rate_permonth))
    # 等额本息
    '''
    每月还款计算公式
    payment_permonth = mortgage* interest_rate_permonth * (1 + interest_rate_permonth)^month / (1 + interest_rate_permonth)^month - 1
    '''
    def equal_cost(self):
        t = math.pow(1 + self.interest_rate_permonth, self.month)
        payment_permonth = round(self.mortgage * self.interest_rate_permonth * t / (t - 1), 2)
        print("每月还款数额:%0.2f元" % payment_permonth)
        print("还款总额:%0.2f元" % (payment_permonth * self.month))
        print("支付的总利息:%0.2f元" % ((payment_permonth * self.month) - self.mortgage))

    def m_print(self):
        print("还款总额:%0.2f" % self.total_payment)
        print("支付的总利息:%0.2f元" % self.total_interest)

class EqualPrincipal(Mortgage):
    def __init__(self, mortgage, month, interest_rate):
        super().__init__(mortgage, month, interest_rate)
        self.__cal()
    def __cal(self):
        self.principal = self.mortgage / self.month
        # 每月还款结果
        self.repayment_arr = []
        for i in range(self.month):
            rest_total = self.mortgage - i * self.principal
            current_interest = rest_total * self.interest_rate_permonth
            repayment = self.principal + current_interest
            self.repayment_arr.append(round(repayment, 2))
        self.total_payment = sum(self.repayment_arr)
        self.total_interest =  self.total_payment- self.mortgage
    def print(self):
        print("等额本金"+ ("="*10))
        print("还款总额:%0.2f" % self.total_payment)
        print("支付总利息:%0.2f" % self.total_interest)
        print("首月还款:%0.2f" % self.repayment_arr[0])
        print("每月还款递减:%0.2f" % (self.principal * self.interest_rate_permonth))
    def __mul__(self, other):
        print("1")
        pass

class EqualCost(Mortgage):
    def __init__(self, mortgage, month, interest_rate):
        super().__init__(mortgage, month, interest_rate)
        self.__cal()
    def __cal(self):
        t = math.pow(1 + self.interest_rate_permonth, self.month)
        self.payment_permonth = round(self.mortgage * self.interest_rate_permonth * t / (t - 1), 2)
        self.total_payment = self.payment_permonth * self.month
        self.total_interest = self.total_payment - self.mortgage
    def print(self):
        print("等额本息"+ ("="*10))
        print("还款总额:%0.2f" % self.total_payment)
        print("支付总利息:%0.2f" % self.total_interest)
        print("每月还款:%0.2f" % self.payment_permonth)
    def prepayment(self, payment, month = 0):
        after_prepayment = EqualCost(self.mortgage - payment, self.month - month, self.interest_rate)
        print("提前还款%d万,缩短%d个月," % (payment/10000, month) + ("="*10))
        print("还款总额减少:%0.2f" % (self.total_payment - after_prepayment.total_payment))
        print("支付总利息减少:%0.2f" % (self.total_interest - after_prepayment.total_interest))
        print("每月还款减少:%0.2f" % (self.payment_permonth - after_prepayment.payment_permonth))
        return self.payment_permonth - after_prepayment.payment_permonth
    def prepayment_chage(self, payment, month = 0):
        after_prepayment = EqualPrincipal(self.mortgage - payment, self.month - month, self.interest_rate)
        first = after_prepayment.repayment_arr[0]
        difference = after_prepayment.principal * after_prepayment.interest_rate_permonth
        print("提前还款%d万,更改还款方式缩短%d个月," % (payment/10000, month) + ("="*10))
        print("还款总额减少:%0.2f" % (self.total_payment - after_prepayment.total_payment))
        print("支付总利息减少:%0.2f" % (self.total_interest - after_prepayment.total_interest))
        print("首月还款:%0.2f" % after_prepayment.repayment_arr[0])
        print("每月还款递减:%0.2f" % (after_prepayment.principal * after_prepayment.interest_rate_permonth))
        return first, difference

class WealthMangement:
    def __init__(self, interest_rate, month, total) -> None:
        self.interest_rate = interest_rate
        self.interest_rate_permonth = interest_rate / 12
        self.month= month
        self.total = total
    # 固定本金复利
    def compound_interest(self):
        all = self.total * math.pow(1 + self.interest_rate_permonth, self.month)
        revenue = all - self.total
        #print("本息和:%0.2f元" % (all))
        #print("总收益:%0.2f元" % (revenue))
        return all, revenue
    # 定投复利
    def regular_investment(self, amount):
        '''
        等比数列
        total = amount * (1 + interest_rate_permonth) * [(1 + interest_rate_permonth)^(month - 1) -1] / interest_rate_permonth
        '''
        self.total = amount * self.month
        t = math.pow(1 + self.interest_rate_permonth, self.month - 1)
        all = amount * (1 + self.interest_rate_permonth) * (t - 1) / self.interest_rate_permonth
        all += amount
        revenue = all - self.total
        #print("总收益:%0.2f元" % all)
        return all, revenue
    # 
    def regular_investment_ch(self, amount, diff):
        pass


if __name__ == "__main__":
    ori_month = 322
    pre_month = 12 * 10
    prepayment = 200000
    #理财收益率
    interest = 0.041
    mort = 628719.95
    #贷款利率
    mort_interest = 0.04

    mortgage = Mortgage(mort, ori_month, mort_interest)
    equal_principal = EqualPrincipal(mort, ori_month, mort_interest)
    equal_principal.print()
    equal_cost = EqualCost(mort, ori_month, mort_interest)
    equal_cost.print()
    amount1 = equal_cost.prepayment(prepayment)
    amount2 = equal_cost.prepayment(prepayment, pre_month)

    amount3, diff1 = equal_cost.prepayment_chage(prepayment)
    amount4, diff2 = equal_cost.prepayment_chage(prepayment, pre_month)

    print("提前还款"+ ("="*10))
    wealth = WealthMangement(interest, ori_month, 0)
    all, revenue = wealth.regular_investment(amount1)
    print("本息和:%0.2f元" % (all))
    print("总收益:%0.2f元" % (all - prepayment))

    wealth1 = WealthMangement(interest, ori_month - pre_month, 0)
    all, revenue = wealth1.regular_investment(amount2)

    print("提前还款,缩短年限"+ ("="*10))
    wealth2 = WealthMangement(interest, pre_month, all)
    all1, revenue1 = wealth2.compound_interest()
    all2, revenue2 = wealth2.regular_investment(3187.32)
    print("本息和:%0.2f元" % (all1 + all2))
    print("总收益:%0.2f元" % (all1 + all2 - prepayment))

    print("理财"+ ("="*10))
    wealth3 = WealthMangement(interest, ori_month, prepayment)
    all, revenue = wealth3.compound_interest()
    print("本息和:%0.2f元" % (all))
    print("总收益:%0.2f元" % (revenue))
    a = WealthMangement(interest, 60, 0)
    all, revenue = a.regular_investment(amount1)
    print("本息和:%0.2f元" % (all))
    print("总收益:%0.2f元" % (revenue))

    #wealth1 = WealthMangement(0.025, 30, 2000)
    #wealth1.compound_interest()
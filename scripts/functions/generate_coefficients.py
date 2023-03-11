import pandas as pd
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")

def generate_coefficients(training_predictors, training_reference_concentrations, method):
    '''
    INPUT...
    training_predictors = dataframe corresponding of predictors in training period 
    training_reference_concentrations = dataframe containing reference concentrations (DEC) during training period
    
    method = 'linear' or 'quadratic' (only LINEAR works as of 02/08/2023)    
    ===========================================================
    RETURNS...
    00 = coefficient + y-intercepts of regression equation as a dictionary (this is what's important!)
    01 = model (kept for documentation purposes)
    '''
    
    if method == 'linear' or method == 'Linear' or method == 'LINEAR':

        #https://www.statology.org/statsmodels-linear-regression-p-value/
        y = training_reference_concentrations
        x = training_predictors
        x = sm.add_constant(x)
        model = sm.OLS(y, x).fit()
        analysis = model.summary()
         
        # coefficient dictionary
        coefs=model.params
        coef_dict={}
        # pvalue dictionary
        pvalues=model.pvalues
        pvalue_dict={}
        
        for num_of_predictors in range(len(coefs)):
            if num_of_predictors == 0:
                coef_dict['Y-intercept (constant term)']=coefs[num_of_predictors]
                pvalue_dict['Y-intercept (constant term)']=pvalues[num_of_predictors]

            else:
                coef_dict[training_predictors.columns[num_of_predictors-1]]=coefs[num_of_predictors]
                pvalue_dict[training_predictors.columns[num_of_predictors-1]]=pvalues[num_of_predictors]
        
        output = {'coef_dict':coef_dict,'pvalue_dict':pvalue_dict,'analysis':analysis,'model':model}
    
        return output
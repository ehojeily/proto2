def calibrate(coef_dict, testing_predictors):
    '''
    INPUT...
    coef_dict = dictionary of regression coefficients generated using the generate_coefficients script 
    testing_data_input = dataframe containing testing concentrations, must include IDENTICAL column names as the training data
    input from the generate_coefficients script to work properly 
    
    ===========================================================
    RETURNS...
    calibrated_data = pandas series that contains date (x) and calibrated data (y)
    '''
        
    calibrated_data = coef_dict['Y-intercept (constant term)']
    print('Beginning calibration... starting with y-intercept = ', calibrated_data)

    for key,value in coef_dict.items():
        if key != 'Y-intercept (constant term)':
            print('Calibrating with coefficient...', coef_dict[key], 'for variable', key)
            calibrated_data += coef_dict[key]*testing_predictors[key]
            print('Coefficient done')
    print('Calibration completed!')
            
    return calibrated_data
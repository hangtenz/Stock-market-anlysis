# Stock-market-anlysis


### Info
    Script to scraping data for analysis SET and VND stock market

### Pipeline of process
    Get quote (get_quote folder)
            |
    store all quote of market in path file/stock-input
            |
    main process for scrapping data
            |
     mark stock which maybe cheap
            |
    store output in file/xlsx
            | 
    store list of interesting stock in file/stock-output 

### Criteria of cheap stock
    With P/E -> have 30 MOS of avg P/E (expected earning = last year of earning)
    With DDM -> have 10% expected return (compute with last year dividend and 3% growth rate)

### Criteria of good stock
    Company has growth in long term = EPS increase every year
    Have power to Negotiate with customers = Gross profit margin is stable
    Be a leader in that sector = SG&A is stable
    Can make the profit in long term = ROE is stable
    Good executives = Cannot measure with number
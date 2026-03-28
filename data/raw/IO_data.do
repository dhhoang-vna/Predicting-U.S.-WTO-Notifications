*============================
* Mancini et al. (2024) data on cross-country global supply chain 
* u_n, u_d: numerator, denominator of upstreamness
* d_n, d_d: numerator, denominator of downstreamness
*============================

clear mata
capture log close
clear

log using "D:\1. M2 Development Economics\2. Big Data Text\Project\gvc_data", replace


import delimited "D:\1. M2 Development Economics\2. Big Data Text\Project\io_sect_isic2_crosswalk.csv", clear varnames(1)
sort source sect
tempfile xwalk
save `xwalk'

use "D:\1. M2 Development Economics\2. Big Data Text\Project\gvc_data.dta", clear
keep if inlist(country, "VNM","THA","IDN","MYS","PHL","MMR","LAO","KHM","TLS")
keep if inrange(t, 2015, 2019)
drop if missing(country) | missing(source) | missing(sect) | missing(t)

isid country source sect t

joinby source sect using `xwalk'

collapse (mean) upstreamness downstreamness u_n u_d d_n d_d, by(country isic2)

* Downstream dependence
gen dd_logU = log(upstreamness)

* IO centrality 
gen centrality = exp(-abs(log(upstreamness) - log(downstreamness)))

export delimited using "io_country_isic2_preavg.csv", replace
save "io_country_isic2_preavg.dta", replace

log close





















library(concordance)
library(dplyr)
library(readr)
library(purrr)

# Read HS4 list from csv
hs_tbl <- read_csv(
  "D:/1. M2 Development Economics/2. Big Data Text/Project/cleaned_data/train_notif_hs4_country_level.csv",
  col_types = cols(hs4 = col_character())
)

hs_vec <- hs_tbl$hs4

# Apply Concordance HS1 to ISIC4
res_list <- concord_hs_isic(
  sourcevar   = hs_vec,
  origin      = "HS6",        # HS2022
  destination = "ISIC4",
  dest.digit  = 2,
  all         = TRUE
)

# Turn list into a table
hs_isic <- map2_dfr(res_list, hs_vec, ~ {
  if (is.null(.x)) return(NULL)
  df <- as.data.frame(.x)
  df$hs4 <- .y
  df
})

# Clean names and keep essential columns
hs_isic <- hs_isic %>%
  rename(isic4 = match,
         share = weight) %>%
  select(hs4, isic4, share)

# Export
setwd("D:/1. M2 Development Economics/2. Big Data Text/Project/cleaned_data")
write_csv(hs_isic, "train_notif_hs4_country_isic4.csv")
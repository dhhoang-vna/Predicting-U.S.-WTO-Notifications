library(concordance)
library(dplyr)
library(readr)
library(purrr)
library(stringr)

R.version.string


# Read full table (keeps all your columns)
df <- read_csv(
  "D:/1. M2 Development Economics/2. Big Data Text/Project/clean_out/train_notif_hs4_country_level.csv",
  col_types = cols(hs4 = col_character())
) |>
  mutate(hs4 = str_pad(hs4, width = 4, side = "left", pad = "0"))

hs_vec <- unique(df$hs4)

# HS -> ISIC4 (2-digit)
# Note: concord_hs_isic supports HS0..HS6 in the github version docs. :contentReference[oaicite:1]{index=1}
res_list <- concord_hs_isic(
  sourcevar   = hs_vec,
  origin      = "HS6",        # use the HS vintage you intend
  destination = "ISIC4",
  dest.digit  = 2,
  all         = TRUE
)

# List -> table
hs_isic <- map2_dfr(res_list, hs_vec, ~{
  if (is.null(.x)) return(NULL)
  tmp <- as.data.frame(.x)
  tmp$hs4 <- .y
  tmp
}) |>
  rename(isic4 = match,
         share = weight) |>
  select(hs4, isic4, share)

# Join back to keep old columns + add isic4/share
df_out <- df |>
  left_join(hs_isic, by = "hs4") |>
  select(notified_document, country, hs4, distribution_date, text, Y_struct_abn, isic4, share)

# Export
write_csv(
  df_out,
  "D:/1. M2 Development Economics/2. Big Data Text/Project/clean_out/train_notif_hs4_country_isic4_2digit_long.csv"
)


##==========================================================##
## R CODE
## Below, we fit a two-part zero-inflated beta mixed model
## in brms() to the data set 'instruments'
##==========================================================##
rm(list=ls())
library(brms)
##----------------------------------------------------------##
# data
instruments <- read.csv(file = "<DIRECTORY_WHERE_REPO_WAS_IMPORTET>/data_results/_tables_/2021-12-08_labeling_instructions_table_v1.0.csv", h = T)

# filter rows | easier display for understanding #
instruments <- instruments[instruments$Instance_ID == 1, ] # filter to single images
instruments <- instruments[instruments$QA == "annotate", ] # remove the qa images

# Invert annotator type 
instruments$Annotator_type_inv[instruments$Annotator_type == "Prof. annotator"] <- "Company_ann" 
instruments$Annotator_type_inv[instruments$Annotator_type == "Crowdworker"] <- "MTurker"

# reassign default value of category to the random category
instruments$category_trans <- factor(instruments$Category, levels = c("09_randomly_selected", "05_simple", "01_chaos",   "02_image_overlay", "03_intersecting", "04_motion_blur", "06_text_overlay", "07_trocar", "08_underexposed"))
instruments$Company=as.factor(instruments$Company)

## response variable used in model
instruments$DSC_img_2part=ifelse(instruments$Image_min_instance_DSC_value==0,0,instruments$DSC_img)

##----------------------------------------------------------##
## fit the model
model=brm(bf(DSC_img_2part ~ Stage+ Annotator_type + category_trans + context_video    + (1|a|Worker_ID) + (1|b|Image_name),zi~Stage+ Annotator_type + category_trans + context_video    + (1|a|Worker_ID) + (1|b|Image_name)),data=instruments,
                 family=zero_inflated_beta(),prior = c(
                   set_prior("normal(0, 10)", class = "b"),
                   set_prior("cauchy(0, 1)", class = "sd")
                 ),chains = 4,iter = 4000,seed = 1234)
summary(model)
##==========================================================##
##==========================================================##

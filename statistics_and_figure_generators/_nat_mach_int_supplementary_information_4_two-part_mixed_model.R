library(lme4)
library(glmmTMB)
library(ggplot2)
library(sjPlot)

##### Import data
data_images<-read.csv("<DIRECTORY_WHERE_REPO_WAS_IMPORTET>/data_results/_tables_/2022-11-10_supplementary_note_4.csv")

# Filter rows | easier display for understanding
data_images <- data_images[data_images$Instance_ID == 1, ] # filter to single images

## Response variable used in model
data_images$DSC_img_2part=ifelse(data_images$Image_min_instance_DSC_value==0,0,data_images$DSC_Img)
data_images[,c(1,2,8:12)]<-lapply(data_images[,c(1,2,8:12)],as.factor)

## Define reference category
data_images<- within(data_images, Labeling_Instruction <- relevel(Labeling_Instruction, ref = "first_labeling_instruction"))

### Create a binary column to use in logistic mixed model
data_images$bin<-as.factor(ifelse(data_images$DSC_img_2part==0,"No","Yes"))

### Fit the model (logistic model valid annotations versus invalid annotations)
mod_bin<-glmer(bin ~ Annotation_Provider_type + (1|Team_name) + (1|Image_name),data=data_images,family=binomial(link = "logit"),
               control=glmerControl(optimizer="bobyqa",optCtrl=list(maxfun=2e5)))
summary(mod_bin)

### Plot the coefficients
plot_model(mod_bin,grid = T,colors = "darkblue",title = "Effect on probability of valid annotations")+
  scale_y_log10(limits = c(0.9, 3))

### Subset to remain with only DSC>0 (Beta mixed model part)
data_images_dsc<-subset(data_images,DSC_img_2part>0)

## Fit the model
mod_cont <- glmmTMB(DSC_img_2part ~ Annotation_Provider_type+ (1|Team_name) + (1|Image_name), data=data_images_dsc, family=list(family="beta",link="logit"))
summary(mod_cont)

## Plot the estimates
plot_model(mod_cont,grid = T,colors = "darkblue",title = "Effect on DSC")+scale_y_log10(limits = c(0.9, 2))

##################
## Labeling instruction type
mod_bin_a<-glmer(bin ~ Labeling_Instruction + (1|Team_name) + (1|Image_name),data=data_images,family=binomial(link = "logit"),
                 control=glmerControl(optimizer="bobyqa",optCtrl=list(maxfun=2e5)))
summary(mod_bin_a)

### Plot the coefficients
plot_model(mod_bin_a,grid = T,title = "Effect on probability of valid annotations")+scale_y_log10(limits = c(0.6, 1.8))

### Subset to remain with only DSC>0 (Beta mixed model part)
data_images_dsc<-subset(data_images,DSC_img_2part>0)

## Fit the model
mod_cont_a <- glmmTMB(DSC_img_2part ~ Labeling_Instruction+ (1|Team_name) + (1|Image_name), data=data_images_dsc, family=list(family="beta",link="logit"))
summary(mod_cont_a)

## Plot the estimates
plot_model(mod_cont_a,grid = T,title = "Effect on DSC")+scale_y_log10(limits = c(0.8, 1.2))
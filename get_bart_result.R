library(rbart)

save.soil <- function(opus.file.path, conf.path, output.file='result.csv', output.path='./'){
  df = read.opus(opus.file.path, conf.path)
  write.csv(df, paste(output.path, output.file, sep=""))
}
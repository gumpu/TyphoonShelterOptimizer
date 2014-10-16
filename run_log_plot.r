require(ggplot2)

dataset <- read.table("runlog.csv", header=TRUE)

p1 <- ggplot(dataset, aes(x=temperature, y=objective)) +
        geom_point() +  scale_x_log10()

ggsave(plot=p1, "runlog.png")



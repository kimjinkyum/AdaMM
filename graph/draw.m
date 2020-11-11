clc, clear, close all

%[GPU,memory]=format_data("data/AdaMM_GPU_usage(timeout=10)_1mix.csv");
%[GPU1,memory1]=format_data("data/AdaMM_GPU_usage(timeout=500)_1video1.csv");

[GPU,memory]=format_data("data/AdaMM_GPU_usage(timeout=10)_1video1.csv");
[GPU1,memory1]=format_data("data/AdaMM_GPU_usage(timeout=10)_1video1.csv");


draw_plot(GPU,GPU1,"GPU usage(timeout 10)", "Adamm","One Server", "GPU usage")
draw_plot(memory,memory1,"GPU Memory(timeout 10)", "Adamm","One Server", "GPU memory (%)")

%Draw plot
function draw_plot(x1,x2,titles,legend1,legend2,ylabels)
X = length(x2);
x1 = x1(1:X);
X1 = 1:X ;
figure
plot(X1,x1,X1,x2)
hold off
legend(legend1,legend2)
title(titles)
xlabel("time")
ylabel(ylabels)

end

function [GPU,memory]=format_data(file_name);
data = readtable(file_name);
Adamm_GPU = data(1,:);
Adamm_memory = data(2,:);
S = vartype("numeric");
position=1;

GPU = Adamm_GPU{:,S};
memory = Adamm_memory{:,S};

for i = 1:size(GPU)
    if GPU(i)~=0
        position=i;
        break;
    end
    
end
GPU= GPU(position,:);
memory = memory(position,:);


end






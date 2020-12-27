clc, clear, close all

%[GPU,memory]=format_data("data/AdaMM_GPU_usage(timeout=10)_1mix.csv");
%[GPU1,memory1]=format_data("data/AdaMM_GPU_usage(timeout=500)_1video1.csv");


%draw_subplot(1)
draw_subplot(4)
%draw_subplot(3)
function draw_subplot(k)
    prob = [0.1,0.3,0.5,0.7]
    x= [10.0,15.0,30.]
    x_=[10,20,30,100]
    a = prob(k)
    tmp = a
    
    
    screensize = get( groot, 'Screensize' )
    sc=[0,0]
    formatSpec = '%.1f';
    t1=tiledlayout(2,3)
    
    x_select = ["10","15","30"];
    y_select = ["Memory utils", "GPU utils(%)"];
    for i = 1:2
        for p = 1:3
            occupy = num2str(x(p),formatSpec);
            file_name_adamm = "last/Prob_"+prob(k)+"occupy time"+ occupy+"Timeout10.0.csv";
            file_name_non = "last/Prob_"+prob(k)+"occupy time"+ occupy+"Timeout500.0.csv";

            %file_name_adamm = "two/Prob_"+prob(k)+"occupy time30.0"+"Timeout"+num2str(x_(p),formatSpec)+".csv";
            %file_name_non = "two/Prob_"+prob(k)+"occupy time30.0"+"Timeout"+num2str(x_(4),formatSpec)+".csv";

            [GPU,memory]=format_data(file_name_adamm);
            [GPU1,memory1]=format_data(file_name_non);

            X = 315;
            %X = 360
            memory = memory(1:X);
            memory1 = memory1(1:X);

            gpu = GPU(1:X);
            gpu1 = GPU1(1:X)
            X1= 1:X;
            nexttile
            if i == 1
                plot(X1, memory, X1, memory1)
                %plot(X1, gpu, X1, gpu1)

                %xticks(0:50:360)
                %xlim([0 365])
                xticks(0:50:315)
                xlim([0,320])
                ylim([0 100])
                title("T = " + num2str(x(p),formatSpec))
                ylabel(y_select(i))
                xlabel("Time(s)")
                
            else
                plot(X1, gpu, X1, gpu1)
                xticks(0:50:315)
                xlim([0,320])
                
                ylim([0 100])
                xlim([0 365])
                %yticks([0,10,20,30,40,50,90,100])
                %yticks(0:20:100)
                title("T = " + num2str(x(p),formatSpec))
                ylabel(y_select(i));
                xlabel("Time(s)");
                
            end
        end
    end
    hold on
legend ("Proposed AdaMM without frame differencing", "Bbaseline",'Location','northoutside')
lgd = legend;
lgd.Layout.Tile = "north";

end



function draw_plot(x1,x2,titles,legend1,legend2,ylabels)
X = 315;
x1 = x1(1:X);
x2 = x2(1:X);
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


GPU= GPU(position,:);
memory = memory(position,:);

end





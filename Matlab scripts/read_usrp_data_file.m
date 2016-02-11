function  x = read_usrp_data_file(filename)

f1 = fopen(filename, 'r');

if (f1 > 0)
    x_tmp = fread(f1, 'float32');
    x = x_tmp(1:2:end)+j*x_tmp(2:2:end);
    y2 = 81:160;
    x2 = x;
    connecty = 80:81;
    connectx = connecty/connecty;
    hold on
    plot(x, 'b')
    plot(connecty, connectx, 'b');
    plot(y2,x2, 'b');
    title('25kbps Transmission Pattern')
    xlabel('sample')
    ylabel('amplitude')
else
    x = -1;
    return
    
end
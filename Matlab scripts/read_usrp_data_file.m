function  x = read_usrp_data_file(filename)

f1 = fopen(filename, 'r');

if (f1 > 0)
    x_tmp = fread(f1, 'float32');
    x = x_tmp(1:2:end)+j*x_tmp(2:2:end);
else
    x = -1
    return
end
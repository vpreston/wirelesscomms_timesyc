function  write_usrp_data_file(x, filename)

f1 = fopen(filename, 'w');

if (f1 > 0)
    x_tmp = zeros(2*length(x), 2);
    x_tmp(1:2:end) = x + x*1j;
    x_tmp(2:2:end) = imag(x);
    x_tmp
    fwrite(f1, x_tmp, 'float32');
else
    x = -1
    return
end

fclose(f1);

end
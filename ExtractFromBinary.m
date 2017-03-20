% Engineer: Thomas Reaney
% Date: 15/02/2017
clear all; close all;

file = fopen("raw18030.bin");
data = fread(file, "ushort");

min = uint16(data(1));
swapped_min = swapbytes(min);

disp(min);
disp(swapped_min);

fclose(file);
% Engineer: Thomas Reaney
% Date: 16/02/2017
clear; clc; close all;

% Get all files ending with .bin in current directory
files = dir("*.bin");
min_tot = 0.0;
max_tot = 0.0;

for i = 1:length(files)
  % Get filename
  filename = files(i).name;
  % Open file
  file = fopen(filename);
  % Read file
  data = fread(file, "ushort");
  
  min_val = int32(swapbytes(uint16(data(1))));
  min_tot += min_val;
  
  max_val = int32(swapbytes(uint16(data(2))));
  max_tot += max_val;
  disp(max_val);
  
  % Close file
  fclose(file);
end

min_avg = min_tot / length(files);
max_avg = max_tot / length(files);
disp(min_avg);
disp(max_avg);
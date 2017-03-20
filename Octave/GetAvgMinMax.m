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
  % Total min values
  min_val = int32(swapbytes(uint16(data(1))));
  min_tot += min_val;
  % Total max values
  max_val = int32(swapbytes(uint16(data(2))));
  max_tot += max_val;
  % Close file
  fclose(file);
end

% Calculate both min and max averages
min_avg = min_tot / length(files);
max_avg = max_tot / length(files);
disp(min_avg);
disp(max_avg);
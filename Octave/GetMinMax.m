% Engineer: Thomas Reaney
% Date: 16/02/2017
clear; clc; close all;

% Get all files ending with .bin in current directory
files = dir("*.bin");

for i = 1:length(files)
  % Get filename
  filename = files(i).name;
  % Open file
  file = fopen(filename);
  % Read file
  data = fread(file, "ushort");
  % Print Values
  disp("\n");
  % disp(filename);
  disp("Min: ");
  disp(swapbytes(uint16(data(1))));
  disp("Max: ");
  disp(swapbytes(uint16(data(2))));
  
  data = data(3:size(data));
  data = reshape(data, [80, 60]);
  disp(data);
  
  % Close file
  fclose(file);
end
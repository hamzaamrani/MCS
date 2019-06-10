clear all;
close all;

collection = dir(fullfile('collection', '*.mat'));
collection = table2struct(sortrows(struct2table(collection), 'bytes'));

for i=1 : size(collection,1)-2
    matrix = load(['collection/',collection(i).name]);

    A = matrix.Problem.A;
    n = length(A);
    xe(1:n,1) = 1;

    disp(['Matrix: ', collection(i).name]);
    disp(['Matrix dimension: ', num2str(size(A,1)), 'x', num2str(size(A,2))]);

    [time, err] = compute(A,xe);
    %mem=get_free_mem();
    %[status, cmdout]=system('sysctl hw.memsize | awk ''{print $2}''');
    
    disp(['Execution time: ', num2str(time), 's']);   %tempo esecuzione
    disp(['Approximation error: ', num2str(err), newline]);    %errore relativo
    clear xe
end

%function to calculate time of execution, approximation error and memory
%usage (missing), use memory(); on Windows
function [time, err ] = compute(A,xe)
    b=A*xe;   

    tic;
    x=A\b;

    time = toc;
    err = norm(x-xe)/norm(xe);
end

function mem=get_free_mem()
    [~,out]=system('vm_stat | grep "Pages free"');
    mem=sscanf(out,'Pages free: %f.');
    mem=mem*4096/1000000000;
end
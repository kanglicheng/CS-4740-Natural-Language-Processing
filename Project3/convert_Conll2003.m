%
% convertTrain.m is used to convert the given train.txt file 
% to the Stanford NER training data format: Each line is a single word 
% and its label separated by a TAB 
%
%

numLines=46435;

fileId = fopen('testb.txt');
fileOUT = fopen('testb.tsv', 'w');
for i=1:numLines
    % each time textscan reads three lines:
    C = textscan(fileId,'%s',1,'Delimiter', '\n');
    % C is a cell
        % actually we won't use the 2nd line tags, but still process it
    S = strsplit(C{1}{1});
    
        %str = [ S{1}(j) char(9) S{3}(j)]
        % first column is the word
    word=char(S(1));
        % 4th column is the label (PER LOC ORG MISC)
    label=char(S(4));
    fprintf(fileOUT,'%s\t%s\n', word, label);
end

ST=fclose(fileId);
ST2=fclose(fileOUT);
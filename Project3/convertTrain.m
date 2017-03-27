%
% convertTrain.m is used to convert the given train.txt file 
% to the Stanford NER training data format: Each line is a single word 
% and its label separated by a TAB 
%
%  word<TAB>Label
%
% Reading the train.txt data file by textscan. In the file, each "sentence"  
% is associated with three lines, as an example below. Each word
% is delimited by a TAB.
%
%  Example sentence in train.txt: 
%
% The following	bond was announced by lead manager Toronto Dominion	.
% DT  VBG	NN	VBD	VBN	IN	NN	NN	NNP	NNP	.
% O 	O	O	O	O	O	O	O	B-PER	I-PER	O
%

numLines=42000;
% every sentence is associated with 3 lines:
numSentence=numLines/3; 

midstop=numSentence/2+1;
fileId = fopen('train.txt');
fileOUT = fopen('stanford_2nd_half.txt', 'w');
for i=midstop:numSentence
    % each time textscan reads three lines:
    C = textscan(fileId,'%s',3,'Delimiter', '\n');
    % C is a cell, C{1}{1} is the first line, C{1}{3} the third line
    % for each "sentence".
    for k=1:3
        % actually we won't use the 2nd line tags, but still process it
        S{k} = strsplit(C{1}{k});
    end
    % slen is the length (number of words) of current line (3-line group):
    slen = length(S{1});
    for j=1:slen
        %str = [ S{1}(j) char(9) S{3}(j)]
        % first row is the word
        word=char(S{1}(j));
        % third row is the label (PER LOC ORG MISC)
        label=char(S{3}(j));
        fprintf(fileOUT,'%s\t%s\n', word, label);
    end

end

ST=fclose(fileId);
ST2=fclose(fileOUT);

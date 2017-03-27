%
% read the NER test file and extract only the text from the
% file, then write out each token in one line to an output file.
%
numLines=9000;
% every sentence is associated with 3 lines:
numSentence=numLines/3; 


fileId = fopen('cornell_test.txt');
fileOUT = fopen('cornell_token.txt', 'w');
for i=1:numSentence
    % each time textscan reads three lines:
    C = textscan(fileId,'%s',3,'Delimiter', '\n');
    % C is a cell, C{1}{1} is the first line, C{1}{3} the third line
    % for each "sentence".
    %
    % S{1} = strsplit(C{1}{1});
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
        lineLabel=char(S{3}(j)); 
        fprintf(fileOUT,'%s\t%s\n', word,lineLabel);
    end

end

ST=fclose(fileId);
ST2=fclose(fileOUT);
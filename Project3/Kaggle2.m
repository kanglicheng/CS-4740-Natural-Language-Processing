function C = Kaggle2
%
fileID=fopen('Kaggle5.dat');
fileOUT=fopen('result2.csv', 'w');
C=textscan(fileID, '%s %f %s');
ST=fclose(fileID);
%   
%  C{1} is the first column (tokens), C{2} the token number, C{3} the tag. 
%  C{1}(1) accesses the first string on the first row
%  C{2}(1) accesses the first number (2nd column) on the first row
%  ...
%  C{3}(k) accesses the third column (the tag) of the k-th row 
%
nData=length(C{1});
NER=[C{3}];  %NER is an array

% NER contains one of the tags: 'I-PER', 'I-LOC', 'I-ORG', 'I-MISC' or 'O'

% Use the power of find() function in Matlab: Ind is an array 
% containing the line number of the match, then we minus one for the
% token (line no.) starts at 0:

fprintf(fileOUT,'Type,Prediction\n');
%------------
Ind=find(strcmp(NER,'I-PER')); 
Ind=Ind-1;  % Test data's tokens starts from 0, so we need to minus 1.
fprintf(fileOUT,'PER,');
disp('PER,')
prediction(Ind, fileOUT);

Ind=find(strcmp(NER,'I-LOC')); 
Ind=Ind-1;
fprintf(fileOUT,'LOC,');
disp('LOC,')
prediction(Ind,fileOUT);

Ind=find(strcmp(NER,'I-ORG')); 
Ind=Ind-1;
fprintf(fileOUT,'ORG,');
disp('ORG,')
prediction(Ind,fileOUT);

Ind=find(strcmp(NER,'I-MISC')); 
Ind=Ind-1;
fprintf(fileOUT,'MISC,');
disp('MISC,')
prediction(Ind,fileOUT);

ST2=fclose(fileOUT);

%
%  function prediction prints out the ranges of PER, LOC, ORG, MISC
%  by using the resepctive Ind array (which contains the
%  line number, i.e., the token position) in the test data file.
%  
function prediction(Ind,fileOUT)
consecutive=0;
num=length(Ind);

for i=1:num
   if consecutive==0
       tag_start=Ind(i);
   end
   
   if (i< num)
       diff=Ind(i+1)-Ind(i);
   end

   if (diff > 1 || i==num) 
       tag_end=Ind(i);
       fprintf(fileOUT, '%d-%d ', tag_start,tag_end);
%       X=sprintf('%d-%d ', tag_start, tag_end);
%       disp(X)
       consecutive=0;
       diff=0;
   elseif (diff == 1)
        consecutive=1;
   end
end
fprintf(fileOUT,'\n');
% end of function prediction









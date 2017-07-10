

function [H_norm, alpha, rpd, intervals, flucts]= rpde_dfa()

load('input.mat','input');

m=4;
tau=35;
[H_norm, rpd] = rpde(input, m, tau);
[alpha, intervals, flucts] = fastdfa(input);
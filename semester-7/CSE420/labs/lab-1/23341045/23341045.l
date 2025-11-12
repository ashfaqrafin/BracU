%option noyywrap
%{
#include<bits/stdc++.h>

#include"symbol_info.h"

#define YYSTYPE symbol_info*

#include "y.tab.h"

    extern YYSTYPE yylval;

    using namespace std;

    void yyerror(char *);


    string loglist;

    extern int lines;

    extern ofstream outlog;

    %}

    /* Regular Definitions */

    delim	 [ \t\v\r]

    /* write regular expressions for whitespace and newline */
    ws		 {delim}+

    newline  \n+

    letter_	 [A-Za-z_]
    digit	 [0-9]

    /* write regular expressions for id, float and integers */
    id		 {letter_}({letter_}|{digit})*
    integer  {digit}+


    %%
{ws}			{ /* ignore whitespace */ }
{newline}	{
    /* do necessary bookkeeping (line number tracking etc.) */
    lines += yyleng;
          }

// Keywords 
int         {
    symbol_info *s = new symbol_info((string)yytext,"INT");
    yylval = (YYSTYPE)s;
    loglist="Line no "+to_string(lines)+": Token <INT> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return INT;
}

float       {
    symbol_info *s = new symbol_info((string)yytext,"FLOAT");
    yylval = (YYSTYPE)s;
    loglist="Line no "+to_string(lines)+": Token <FLOAT> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return FLOAT;
}

void        {
    symbol_info *s = new symbol_info((string)yytext,"VOID");
    yylval = (YYSTYPE)s;
    loglist="Line no "+to_string(lines)+": Token <VOID> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return VOID;
}

return      {
    symbol_info *s = new symbol_info((string)yytext,"RETURN");
    yylval = (YYSTYPE)s;
    loglist="Line no "+to_string(lines)+": Token <RETURN> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return RETURN;
}

if          { 
    loglist="Line no "+to_string(lines)+": Token <IF> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return IF; }

    else        {
        loglist="Line no "+to_string(lines)+": Token <ELSE> Lexeme "+yytext+" found"+"\n"+"\n";
        outlog<<loglist;
        return ELSE;
    }


for         {
    loglist="Line no "+to_string(lines)+": Token <FOR> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist; 
    return FOR; }

    while       { 
        loglist="Line no "+to_string(lines)+": Token <WHILE> Lexeme "+yytext+" found"+"\n"+"\n";
        outlog<<loglist; 
        return WHILE; }

        printf      {
            loglist="Line no "+to_string(lines)+": Token <PRINTLN> Lexeme "+yytext+" found"+"\n"+"\n";
            outlog<<loglist;
            return PRINTLN;
        }


if          { 
    loglist="Line no "+to_string(lines)+": Token <IF> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return IF; }

    while       { 
        loglist="Line no "+to_string(lines)+": Token <WHILE> Lexeme "+yytext+" found"+"\n"+"\n";
        outlog<<loglist; 
        return WHILE; }

        "+"|"-"	    {
            symbol_info *s = new symbol_info((string)yytext,"ADDOP");
            yylval = (YYSTYPE)s;
            loglist="Line no "+to_string(lines)+": Token <ADDOP> Lexeme "+yytext+" found"+"\n"+"\n";
            outlog<<loglist;
            return ADDOP;
        }

{id}       {
    symbol_info *s = new symbol_info((string)yytext,"ID");
    yylval = (YYSTYPE)s;
    loglist="Line no "+to_string(lines)+": Token <ID> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return ID;
           }

// Operator and Punctuation Tokens

"&&"|"||" {
    symbol_info *s = new symbol_info((string)yytext,"LOGICOP");
    yylval = (YYSTYPE)s;
    loglist="Line no "+to_string(lines)+": Token <LOGICOP> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return LOGICOP;
}

"=="|"!="|"<="|">="|"<"|">" {
    symbol_info *s = new symbol_info((string)yytext,"RELOP");
    yylval = (YYSTYPE)s;
    loglist="Line no "+to_string(lines)+": Token <RELOP> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return RELOP;
}

"+"|"-"	    {
    symbol_info *s = new symbol_info((string)yytext,"ADDOP");
    yylval = (YYSTYPE)s;
    loglist="Line no "+to_string(lines)+": Token <ADDOP> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return ADDOP;
}

"*"|"/"|"%" {
    symbol_info *s = new symbol_info((string)yytext,"MULOP");
    yylval = (YYSTYPE)s;
    loglist="Line no "+to_string(lines)+": Token <MULOP> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return MULOP;
}

"="        {
    loglist="Line no "+to_string(lines)+": Token <ASSIGNOP> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;               
    return ASSIGNOP; }

    "!"        {
        loglist="Line no "+to_string(lines)+": Token <NOT> Lexeme "+yytext+" found"+"\n"+"\n";
        outlog<<loglist;
        return NOT;
    }

","        { 
    loglist="Line no "+to_string(lines)+": Token <COMMA> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;               
    return COMMA; }

    ";"        {
        loglist="Line no "+to_string(lines)+": Token <SEMICOLON> Lexeme "+yytext+" found"+"\n"+"\n";
        outlog<<loglist;
        return SEMICOLON;
    }

"("        {
    loglist="Line no "+to_string(lines)+": Token <LPAREN> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return LPAREN;
}

")"        {
    loglist="Line no "+to_string(lines)+": Token <RPAREN> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return RPAREN;
}

"{"        {
    loglist="Line no "+to_string(lines)+": Token <LCURL> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return LCURL;
}

"}"        {
    loglist="Line no "+to_string(lines)+": Token <RCURL> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return RCURL;
}

"["        {
    loglist="Line no "+to_string(lines)+": Token <LTHIRD> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return LTHIRD;
}

"]"        {
    loglist="Line no "+to_string(lines)+": Token <RTHIRD> Lexeme "+yytext+" found"+"\n"+"\n";
    outlog<<loglist;
    return RTHIRD;
}


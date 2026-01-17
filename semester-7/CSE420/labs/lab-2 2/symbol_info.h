#include <bits/stdc++.h>
using namespace std;

class symbol_info
{
private:
    string name; 
    string type; 

    string data_type;                        
    string symbol_kind;                      
    int array_size = -1;                     
    vector<pair<string, string>> parameters; 

public:
    symbol_info(string name, string type)
    {
        this->name = name;
        this->type = type;
    }

    string getname() const { return name; }
    string get_type() const { return type; }
    string get_name() const { return name; }
    void setname(const string &n) { name = n; }
    void set_name(const string &n) { name = n; }
    void set_type(const string &t) { type = t; }

    void set_data_type(const string &t) { data_type = t; }
    string get_data_type() const { return data_type; }

    void set_kind(const string &k) { symbol_kind = k; }
    string get_kind() const { return symbol_kind; }

    void set_array_size(int sz) { array_size = sz; }
    int get_array_size() const { return array_size; }

    void clear_parameters() { parameters.clear(); }
    void add_parameter(const string &ptype, const string &pname)
    {
        parameters.emplace_back(ptype, pname);
    }
    void set_parameters(const vector<pair<string, string>> &params)
    {
        parameters = params;
    }
    const vector<pair<string, string>> &get_parameters() const { return parameters; }

    ~symbol_info() {}
};

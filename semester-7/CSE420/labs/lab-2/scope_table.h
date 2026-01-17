#include "symbol_info.h"

class scope_table
{
    private:
        int bucket_count;
        int unique_id;
        scope_table *parent_scope = NULL;
        vector<list<symbol_info *>> table;

        int hash_function(string name)
        {
            unsigned long long sum = 0;
            for(char c : name) sum += static_cast<unsigned char>(c);
            return (int)(sum % bucket_count);
        }

    public:
        scope_table();
        scope_table(int bucket_count, int unique_id, scope_table *parent_scope);
        scope_table *get_parent_scope();
        int get_unique_id();
        symbol_info *lookup_in_scope(symbol_info* symbol);
        bool insert_in_scope(symbol_info* symbol);
        bool delete_from_scope(symbol_info* symbol);
        void print_scope_table(ofstream& outlog);
        ~scope_table();
};

// complete the methods of scope_table class
void scope_table::print_scope_table(ofstream& outlog)
{
    outlog << "ScopeTable # "+ to_string(unique_id) << endl;

    for(int i=0;i<bucket_count;i++)
    {
        if(table[i].empty()) continue;
        outlog << i << " --> " << endl;
        for(auto *sym : table[i])
        {
            outlog << "< " << sym->getname() << " : " << sym->get_type() << " >" << endl;
            const string kind = sym->get_kind();
            if(kind == "Variable")
            {
                outlog << "Variable" << endl;
                outlog << "Type: " << sym->get_data_type() << endl;
            }
            else if(kind == "Array")
            {
                outlog << "Array" << endl;
                outlog << "Type: " << sym->get_data_type() << endl;
                outlog << "Size: " << sym->get_array_size() << endl;
            }
            else if(kind == "Function Declaration" || kind == "Function Definition")
            {
                outlog << kind << endl;
                outlog << "Return Type: " << sym->get_data_type() << endl;
                const auto &params = sym->get_parameters();
                outlog << "Number of Parameters: " << params.size() << endl;
                outlog << "Parameter Details: ";
                for(size_t j=0;j<params.size();j++)
                {
                    outlog << params[j].first;
                    if(!params[j].second.empty()) outlog << " " << params[j].second;
                    if(j+1<params.size()) outlog << ", ";
                }
                outlog << endl;
            }
            // blank line after each symbol per sample output
            outlog << endl;
        }
    }
}

// Implementations
scope_table::scope_table(): bucket_count(10), unique_id(0), parent_scope(NULL), table(10) {}

scope_table::scope_table(int bucket_count, int unique_id, scope_table *parent_scope)
    : bucket_count(bucket_count), unique_id(unique_id), parent_scope(parent_scope), table(bucket_count) {}

    scope_table* scope_table::get_parent_scope() { return parent_scope; }
    int scope_table::get_unique_id() { return unique_id; }

symbol_info* scope_table::lookup_in_scope(symbol_info* symbol)
{
    if(symbol == NULL) return NULL;
    int idx = hash_function(symbol->getname());
    for(auto *s : table[idx])
    {
        if(s->getname() == symbol->getname()) return s;
    }
    return NULL;
}

bool scope_table::insert_in_scope(symbol_info* symbol)
{
    if(symbol == NULL) return false;
    if(lookup_in_scope(symbol) != NULL) return false; // already exists in current scope
    int idx = hash_function(symbol->getname());
    table[idx].push_back(symbol);
    return true;
}

bool scope_table::delete_from_scope(symbol_info* symbol)
{
    if(symbol == NULL) return false;
    int idx = hash_function(symbol->getname());
    for(auto it = table[idx].begin(); it != table[idx].end(); ++it)
    {
        if((*it)->getname() == symbol->getname())
        {
            delete *it;
            table[idx].erase(it);
            return true;
        }
    }
    return false;
}

scope_table::~scope_table()
{
    for(auto &lst : table)
    {
        for(auto *s : lst) delete s;
        lst.clear();
    }
}

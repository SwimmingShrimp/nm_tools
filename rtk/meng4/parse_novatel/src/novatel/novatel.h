#pragma once

#include <string>
#include <iostream>
#include <vector>
#include <fstream>

struct MsgItem
{
    std::string item_name;
    std::string item_unit;
    std::string item_separator;
    bool item_visible;
};

class Novatel
{
public:
    Novatel();
    ~Novatel();
    bool Parse(const std::string &parse_file);

private:
    bool WriteItemTitle(std::ofstream &ofstream_out, const std::vector<MsgItem> &item_list, std::string file_name);
    bool ParseMsg(std::ofstream &ofstream_out, const std::string &str_msg, const std::vector<MsgItem> &item_list);
    void LineParse(const std::string &str_line);

    const std::vector<std::string> msg_typr_flag = {"%RAWIMUSA", "#INSPVAXA", "$GPGGA", "$GPRMC", "$GPGSA"};

    std::vector<MsgItem> rawimusa_msg_;
    std::vector<MsgItem> inspvaxa_msg_;
    std::vector<MsgItem> gpgga_msg_;
    std::vector<MsgItem> gprmc_msg_;
    std::vector<MsgItem> gpgsa_msg_;

    std::ofstream rawimusa_ofstream_;
    std::ofstream inspvaxa_ofstream_;
    std::ofstream gpgga_ofstream_;
    std::ofstream gprmc_ofstream_;
    std::ofstream gpgsa_ofstream_;
};
#include "novatel.h"

Novatel::Novatel()
{

    rawimusa_msg_.push_back({"TimeStamp", "", ",", true});
    rawimusa_msg_.push_back({"MsgType", "", ",", true});
    rawimusa_msg_.push_back({"Week Number", "", ",", true});
    rawimusa_msg_.push_back({"Seconds", "", ";", true});
    rawimusa_msg_.push_back({"GNSS Week", "", ",", true});
    rawimusa_msg_.push_back({"Seconds into Week", "", ",", true});
    rawimusa_msg_.push_back({"IMU Status", "", ",", true});
    rawimusa_msg_.push_back({"Z Accel Output", "", ",", true});
    rawimusa_msg_.push_back({"-(Y Accel Output)", "", ",", true});
    rawimusa_msg_.push_back({"X Accel Output", "", ",", true});
    rawimusa_msg_.push_back({"Z Gyro Output", "", ",", true});
    rawimusa_msg_.push_back({"-(Y Gyro Output)", "", ",", true});
    rawimusa_msg_.push_back({"X Gyro Output", "", "*", true});

    inspvaxa_msg_.push_back({"TimeStamp", "", ",", true});
    inspvaxa_msg_.push_back({"MsgType", "", ",", true});
    inspvaxa_msg_.push_back({"Port", "", ",", true});
    inspvaxa_msg_.push_back({"Sequence", "", ",", true});
    inspvaxa_msg_.push_back({"% Idle Time", "", ",", true});
    inspvaxa_msg_.push_back({"Time Status", "", ",", true});
    inspvaxa_msg_.push_back({"Week", "", ",", true});
    inspvaxa_msg_.push_back({"Seconds", "", ",", true});
    inspvaxa_msg_.push_back({"Receiver Status", "", ",", true});
    inspvaxa_msg_.push_back({"Reserved", "", ",", true});
    inspvaxa_msg_.push_back({"Receiver S/W Version", "", ";", true});
    inspvaxa_msg_.push_back({"INS Status", "", ",", true});
    inspvaxa_msg_.push_back({"Pos Type", "", ",", true});
    inspvaxa_msg_.push_back({"Latitude ", "", ",", true});
    inspvaxa_msg_.push_back({"Longitude", "", ",", true});
    inspvaxa_msg_.push_back({"Height", "m", ",", true});
    inspvaxa_msg_.push_back({"Undulation", "m", ",", true});
    inspvaxa_msg_.push_back({"North velocity", "m/s", ",", true});
    inspvaxa_msg_.push_back({"East velocity", "m/s", ",", true});
    inspvaxa_msg_.push_back({"Up velocity", "m/s", ",", true});
    inspvaxa_msg_.push_back({"Roll", "", ",", true});
    inspvaxa_msg_.push_back({"Pitch", "", ",", true});
    inspvaxa_msg_.push_back({"Azimuth", "", ",", true});
    inspvaxa_msg_.push_back({"Latitude standard deviation", "m", ",", true});
    inspvaxa_msg_.push_back({"Longitude standard deviation", "m", ",", true});
    inspvaxa_msg_.push_back({"Height standard deviation", "m", ",", true});
    inspvaxa_msg_.push_back({"North velocity standard deviation", "m/s", ",", true});
    inspvaxa_msg_.push_back({"East velocity standard deviation", "m/s", ",", true});
    inspvaxa_msg_.push_back({"Up velocity standard deviation", "m/s", ",", true});
    inspvaxa_msg_.push_back({"Roll standard deviation", "", ",", true});
    inspvaxa_msg_.push_back({"Pitch standard deviation", "", ",", true});
    inspvaxa_msg_.push_back({"Azimuth standard deviation", "", ",", true});
    inspvaxa_msg_.push_back({"Extended solution status", "", ",", true});
    inspvaxa_msg_.push_back({"Time Since Update", "", "*", true});

    gpgga_msg_.push_back({"TimeStamp", "", ",", true});
    gpgga_msg_.push_back({"MsgType", "", ",", true});
    gpgga_msg_.push_back({"UTC time", "hhmmss.ss", ",", true});
    gpgga_msg_.push_back({"Latitude", "DDmm.mm", ",", true});
    gpgga_msg_.push_back({"Latitude direction", "", ",", true});
    gpgga_msg_.push_back({"Longitude", "DDDmm.mm", ",", true});
    gpgga_msg_.push_back({"Longitude direction", "", ",", true});
    gpgga_msg_.push_back({"GPS Quality", "", ",", true});
    gpgga_msg_.push_back({"Number of satellites in use", "", ",", true});
    gpgga_msg_.push_back({"Horizontal dilution of precision", "", ",", true});
    gpgga_msg_.push_back({"Antenna altitude", "", ",", true});
    gpgga_msg_.push_back({"Antenna altitude Units", "", ",", true});
    gpgga_msg_.push_back({"Undulation", "", ",", true});
    gpgga_msg_.push_back({"Units of undulation", "", ",", true});
    gpgga_msg_.push_back({"Age of correction data", "s", ",", true});
    gpgga_msg_.push_back({"station ID", "", "*", true});

    gprmc_msg_.push_back({"TimeStamp", "", ",", true});
    gprmc_msg_.push_back({"MsgType", "", ",", true});
    gprmc_msg_.push_back({"UTC", "hhmmss.ss", ",", true});
    gprmc_msg_.push_back({"Position status", "", ",", true});
    gprmc_msg_.push_back({"Latitude", "DDmm.mm", ",", true});
    gprmc_msg_.push_back({"Latitude direction", "", ",", true});
    gprmc_msg_.push_back({"Longitude", "DDDmm.mm", ",", true});
    gprmc_msg_.push_back({"Longitude direction", "", ",", true});
    gprmc_msg_.push_back({"speed Kn", "", ",", true});
    gprmc_msg_.push_back({"track true", "", ",", true});
    gprmc_msg_.push_back({"date", "dd_mm_yy", ",", true});
    gprmc_msg_.push_back({"Magnetic variation", "", ",", true});
    gprmc_msg_.push_back({"Magnetic variation direction", "", ",", true});
    gprmc_msg_.push_back({"mode indicator", "", "*", true});

    gpgsa_msg_.push_back({"TimeStamp", "", ",", true});
    gpgsa_msg_.push_back({"MsgType", "", ",", true});
    gpgsa_msg_.push_back({"mode MA", "A=Automatic/M=Manual", ",", true});
    gpgsa_msg_.push_back({"mode 123", "", ",", true});
    gpgsa_msg_.push_back({"prn", "", ",", true});
    gpgsa_msg_.push_back({"prn", "", ",", true});
    gpgsa_msg_.push_back({"prn", "", ",", true});
    gpgsa_msg_.push_back({"prn", "", ",", true});
    gpgsa_msg_.push_back({"prn", "", ",", true});
    gpgsa_msg_.push_back({"prn", "", ",", true});
    gpgsa_msg_.push_back({"prn", "", ",", true});
    gpgsa_msg_.push_back({"prn", "", ",", true});
    gpgsa_msg_.push_back({"prn", "", ",", true});
    gpgsa_msg_.push_back({"prn", "", ",", true});
    gpgsa_msg_.push_back({"prn", "", ",", true});
    gpgsa_msg_.push_back({"prn", "", ",", true});
    gpgsa_msg_.push_back({"Position dilution of precision", "", ",", true});
    gpgsa_msg_.push_back({"Horizontal dilution of precision", "", ",", true});
    gpgsa_msg_.push_back({"Vertical dilution of precision", "", "*", true});

    WriteItemTitle(rawimusa_ofstream_, rawimusa_msg_, msg_typr_flag[0]);
    WriteItemTitle(inspvaxa_ofstream_, inspvaxa_msg_, msg_typr_flag[1]);
    WriteItemTitle(gpgga_ofstream_, gpgga_msg_, msg_typr_flag[2]);
    WriteItemTitle(gprmc_ofstream_, gprmc_msg_, msg_typr_flag[3]);
    WriteItemTitle(gpgsa_ofstream_, gpgsa_msg_, msg_typr_flag[4]);
}

Novatel::~Novatel()
{
}

bool Novatel::WriteItemTitle(std::ofstream &ofstream_out, const std::vector<MsgItem> &item_list, std::string file_name)
{
    ofstream_out.open((file_name.substr(1) + ".csv").c_str());
    for (auto iter = item_list.begin(); iter != item_list.end(); ++iter)
    {
        if (iter == item_list.begin())
        {
            ofstream_out << iter->item_name;
        }
        else
        {
            ofstream_out << "," << iter->item_name;
        }
        if (!iter->item_unit.empty())
        {
            ofstream_out << "(" << iter->item_unit << ")";
        }
    }

    ofstream_out << "\n";
    return true;
}

bool Novatel::ParseMsg(std::ofstream &ofstream_out, const std::string &str_msg, const std::vector<MsgItem> &item_list)
{
    std::size_t pos_pre = 0;
    std::size_t pos_find = 0;
    std::vector<std::string> value_list;

    for (auto iter : item_list)
    {
        pos_find = str_msg.find_first_of(iter.item_separator, pos_pre);
        if (pos_find == std::string::npos)
        {
            std::cout << "find" << iter.item_name << "fail!" << str_msg << std::endl;
            return false;
        }
        std::string str_tmp = str_msg.substr(pos_pre, pos_find - pos_pre);
        if (str_tmp.length() > 20)
        {
            std::cout << "Item to long:" << str_msg << std::endl;
            return false;
        }

        value_list.push_back(str_tmp);

        pos_pre = pos_find + 1;
    }

    for (auto iter = value_list.begin(); iter != value_list.end(); ++iter)
    {
        if (iter == value_list.begin())
        {
            ofstream_out << *iter;
        }
        else
        {
            ofstream_out << "," << *iter;
        }
    }

    ofstream_out << "\n";
    return true;
}

void Novatel::LineParse(const std::string &str_line)
{

    if (str_line.find(msg_typr_flag[0]) != std::string::npos)
    {
        ParseMsg(rawimusa_ofstream_, str_line, rawimusa_msg_);
    }
    else if (str_line.find(msg_typr_flag[1]) != std::string::npos)
    {
        ParseMsg(inspvaxa_ofstream_, str_line, inspvaxa_msg_);
    }
    else if (str_line.find(msg_typr_flag[2]) != std::string::npos)
    {
        ParseMsg(gpgga_ofstream_, str_line, gpgga_msg_);
    }
    else if (str_line.find(msg_typr_flag[3]) != std::string::npos)
    {
        ParseMsg(gprmc_ofstream_, str_line, gprmc_msg_);
    }
    else if (str_line.find(msg_typr_flag[4]) != std::string::npos)
    {
        ParseMsg(gpgsa_ofstream_, str_line, gpgsa_msg_);
    }

}

bool Novatel::Parse(const std::string &parse_file)
{
    std::ifstream in_file(parse_file, std::ifstream::in);

    if (!in_file.is_open())
    {
        std::cerr << "open novatel file failed ." << std::endl;
        return false;
    }

    std::string line_read;

    while (getline(in_file, line_read))
    {
        LineParse(line_read);
    }

    in_file.close();

    rawimusa_ofstream_.close();
    inspvaxa_ofstream_.close();
    gpgga_ofstream_.close();
    gprmc_ofstream_.close();
    gpgsa_ofstream_.close();
}
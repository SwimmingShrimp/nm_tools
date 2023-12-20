import csv
import rosbag
from bagpy import bagreader

src = '/home/lixialin/Downloads/fusion.bag'

bag_data = rosbag.Bag(src)
print(bag_data)

# 命令行：将topic保存成csv
# rostopic echo -b xxx.bag -p /topic_name > xxx.csv

# topic自动提取保存为csv
# Bag = bagreader(src)
# perception_topic = Bag.message_by_topic("/perception/front_far_obstacle")

# topics:      /aeb/aeb_object_predict_trajectory_array            12327 msgs @ 40.8 Hz : nullmax_msgs/ObjectTrajectoryArray         
#              /aeb/aebs_control_c_command                         12327 msgs @ 40.9 Hz : nullmax_msgs/AebsControlCCommand           
#              /aeb/aebs_event                                         1 msg            : nullmax_msgs/AebsEvent                     
#              /aeb/aebs_monitor                                   12326 msgs @ 23.9 Hz : vehicle_monitor_msgs/AebsMonitor           
#              /aeb/aebs_monitor_string                            12327 msgs @ 37.3 Hz : vehicle_monitor_msgs/AebsMonitorString     
#              /control/control_input                               5810 msgs @ 19.2 Hz : nullmax_msgs/ControlInput                  
#              /control/mcu_to_soc_ctrl_monitor                    15032 msgs @ 50.5 Hz : nullmax_msgs/McuToSocControlMonitor        
#              /fusion/camera_process/processed_camera_obstacles    3621 msgs @ 11.9 Hz : nullmax_msgs/CameraObstacleArray           
#              /fusion/front_freespace_contour                      3620 msgs @ 11.8 Hz : nullmax_msgs/FreeSpaceContour              
#              /fusion/fused_lane_array                             3620 msgs @ 11.9 Hz : nullmax_msgs/FusedLaneArray                
#              /fusion/low_speed_fused_freespace_contour           13976 msgs @ 46.5 Hz : nullmax_msgs/FusedFreeSpaceContour         
#              /fusion/obstacle_list                                9000 msgs @ 25.8 Hz : nullmax_msgs/FusedObstacleArray            
#              /fusion/radar_process/processed_radar_tracks         7300 msgs @ 22.8 Hz : nullmax_msgs/RadarObstacleArray            
#              /fusion/sonar_freespace_contour                      5967 msgs @ 22.1 Hz : nullmax_msgs/FusedFreeSpaceContour         
#              /heart_beat/aebs_heart_beat                         12327 msgs @ 40.9 Hz : std_msgs/Bool                              
#              /heart_beat/planning_heart_beat                      5812 msgs @ 18.9 Hz : std_msgs/Bool                              
#              /heart_beat/sensing_heart_beat                      13976 msgs @ 46.5 Hz : std_msgs/Bool                              
#              /hmi_cfg/parameter_updates                              1 msg            : dynamic_reconfigure/Config                 
#              /localization/localization_request                     38 msgs @  0.5 Hz : nullmax_msgs/LocalizationReq               
#              /lss/lateral_cmd                                     2034 msgs @ 19.2 Hz : nullmax_msgs/LssLateralControlCommand      
#              /mona/bosch/front_radar_raw_tracks                   7296 msgs @ 22.7 Hz : nullmax_msgs/MonaBoschFrontRadarInfoArray  
#              /mona/desay/front_corner_radar_raw_tracks            7127 msgs @ 22.8 Hz : nullmax_msgs/MonaDesayCornerRadarTrackArray
#              /mona/desay/rear_corner_radar_raw_tracks             7127 msgs @ 22.8 Hz : nullmax_msgs/MonaDesayCornerRadarTrackArray
#              /mona/mona_acc_state_output                         15027 msgs @ 56.2 Hz : mona_msgs/MonaAccStateOutput               
#              /mona/mona_aebs_state_output                        15026 msgs @ 56.3 Hz : mona_msgs/MonaAEBStateOutput               
#              /mona/mona_ihc_state_output                         15021 msgs @ 56.4 Hz : mona_msgs/MonaIhcStateOutput               
#              /mona/mona_lss_state_output                         15021 msgs @ 56.3 Hz : mona_msgs/MonaLssStateOutput               
#              /mona/mona_pilot_state_output                       15021 msgs @ 56.2 Hz : mona_msgs/MonaPilotStateOutput             
#              /mona/mona_tsr_state_output                         15014 msgs @ 56.5 Hz : mona_msgs/MonaTsrStateOutput               
#              /mona/uss/uss_raw_tracks                             6006 msgs @ 21.8 Hz : nullmax_msgs/MonaUssReport                 
#              /mona_state/mona_acc_input                           5805 msgs @ 19.1 Hz : mona_msgs/MonaAccInfo                      
#              /mona_state/mona_aebs_state_input                   12312 msgs @ 40.8 Hz : nullmax_msgs/MonaAebInfo                   
#              /mona_state/mona_bsd_input                           5805 msgs @ 19.2 Hz : mona_msgs/MonaBSDInfo                      
#              /mona_state/mona_dclc_input                          5805 msgs @ 19.0 Hz : mona_msgs/MonaDCLCInfo                     
#              /mona_state/mona_dclc_to_hmi                         5805 msgs @ 19.0 Hz : mona_msgs/MonaDCLCToHmi                    
#              /mona_state/mona_dow_input                           5805 msgs @ 19.2 Hz : mona_msgs/MonaDOWInfo                      
#              /mona_state/mona_elk_input                           5805 msgs @ 19.0 Hz : mona_msgs/MonaElkInfo                      
#              /mona_state/mona_fcta_input                         12312 msgs @ 40.9 Hz : mona_msgs/MonaFCTAInfo                     
#              /mona_state/mona_fctb_input                         12312 msgs @ 40.8 Hz : mona_msgs/MonaFCTBInfo                     
#              /mona_state/mona_icc_input                           5804 msgs @ 19.4 Hz : mona_msgs/MonaIccInfo                      
#              /mona_state/mona_ihc_input                           3615 msgs @ 12.4 Hz : mona_msgs/MonaIhcInfo                      
#              /mona_state/mona_lcw_input                           5803 msgs @ 19.1 Hz : mona_msgs/MonaLCWInfo                      
#              /mona_state/mona_ldp_input                           5803 msgs @ 19.1 Hz : mona_msgs/MonaLdpInfo                      
#              /mona_state/mona_rcta_input                         12308 msgs @ 40.9 Hz : mona_msgs/MonaRCTAInfo                     
#              /mona_state/mona_rctb_input                         12308 msgs @ 40.9 Hz : mona_msgs/MonaRCTBInfo                     
#              /mona_state/mona_rcw_input                           5803 msgs @ 19.1 Hz : mona_msgs/MonaRCWInfo                      
#              /mona_state/mona_tsr_input                          13954 msgs @ 46.5 Hz : mona_msgs/MonaTsrInfo                      
#              /odom/current_pose                                  10860 msgs @ 44.6 Hz : geometry_msgs/PoseStamped                  
#              /perception/freespace_contour                        3615 msgs @ 12.1 Hz : nullmax_msgs/FreeSpaceContour              
#              /perception/injected_obstacle_list                   5928 msgs @ 19.8 Hz : nullmax_msgs/FusedObstacleArray            
#              /perception/injection_obstacle_groundtruth           5928 msgs @ 19.8 Hz : nullmax_msgs/InjectionObstacleInfo         
#              /perception/lka_lane_list                            3615 msgs @ 12.1 Hz : nullmax_msgs/LkaLaneArray                  
#              /perception/obstacle_list                            3615 msgs @ 12.4 Hz : nullmax_msgs/CameraObstacleArray           
#              /perception/rotation_matrix_world_2_uv               3615 msgs @ 12.4 Hz : nullmax_msgs/RotationMatrix                
#              /perception/traffic_lights                           3614 msgs @ 12.4 Hz : nullmax_msgs/TrafficLightGroupList         
#              /perception/traffic_signs                            3614 msgs @ 12.4 Hz : nullmax_msgs/TrafficSignMsgList            
#              /planning/control_c_command                          5799 msgs @ 19.2 Hz : nullmax_msgs/ControlCommand                
#              /planning/planning_state                             5799 msgs @ 18.9 Hz : nullmax_msgs/PlanningState                 
#              /planning/trajectory_reference_line                  4744 msgs @ 19.5 Hz : nullmax_msgs/TrajectoryReferenceLine       
#              /planning/vehicle_monitor                            5797 msgs @ 19.8 Hz : vehicle_monitor_msgs/VehicleMonitor        
#              /planning/vehicle_monitor_string                     5797 msgs @ 19.8 Hz : vehicle_monitor_msgs/VehicleMonitorString  
#              /sas/sas_state                                       4648 msgs @ 15.5 Hz : vehicle_monitor_msgs/SasState              
#              /sensing/bcm_report                                 14998 msgs @ 57.1 Hz : vehicle_msgs/BcmReport                     
#              /sensing/ego_car_state                              10854 msgs @ 44.7 Hz : nullmax_msgs/EgoCarState                   
#              /sensing/ems_report                                 14999 msgs @ 56.9 Hz : vehicle_msgs/EmsReport                     
#              /sensing/eps_report                                 14999 msgs @ 56.6 Hz : vehicle_msgs/EpsReport                     
#              /sensing/esp_report                                 14999 msgs @ 56.7 Hz : vehicle_msgs/EspReport                     
#              /sensing/esp_speed_report                           14999 msgs @ 56.8 Hz : vehicle_msgs/EspSpeedReport                
#              /sensing/frequency_state                             4648 msgs @ 15.5 Hz : vehicle_monitor_msgs/FrequencyState        
#              /sensing/hmi_report                                 14998 msgs @ 57.2 Hz : vehicle_msgs/HmiReport                     
#              /sensing/imu_report                                 14998 msgs @ 57.0 Hz : sensor_msgs/Imu                            
#              /sensing/speed_limits                                4648 msgs @ 15.5 Hz : nullmax_msgs/SpeedLimitArray               
#              /sensing/switch_report                              10854 msgs @ 44.1 Hz : vehicle_msgs/SwitchReport                  
#              /sensing/system_failure                              4648 msgs @ 15.5 Hz : nullmax_msgs/SystemFailureArray            
#              /sensing/tcu_report                                 14999 msgs @ 56.6 Hz : vehicle_msgs/TcuReport                     
#              /vehicle/gear_report                                14993 msgs @ 57.1 Hz : vehicle_msgs/GearReport                    
#              /vehicle/throttle_report                            14993 msgs @ 57.3 Hz : vehicle_msgs/ThrottleReport                
#              /vehicle/turn_signal_cmd                             5795 msgs @ 19.2 Hz : vehicle_msgs/TurnSignalCmd                 
#              /vehicle/twist                                      10850 msgs @ 44.3 Hz : nullmax_msgs/TwistStamped
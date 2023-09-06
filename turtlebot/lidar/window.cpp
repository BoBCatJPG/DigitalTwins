#include "renderarea.h"
#include "window.h"

#include <iostream>
#include <QtWidgets>

const int IdRole = Qt::UserRole;

Window::Window() :
  QWidget(),
  angular_min_(0),
  angular_max_(360),
  radial_min_(0),
  radial_max(4000),
  baud_rate_(230400),
  port_("/dev/ttyUSB0"),
  shutting_down_(false),
  serial_(io_, port_)
{
    renderArea = new RenderArea;
    QGridLayout *mainLayout = new QGridLayout;
    mainLayout->setColumnStretch(0, 1);
    mainLayout->setColumnStretch(3, 1);
    mainLayout->addWidget(renderArea, 0, 0, 1, 4);
    setLayout(mainLayout);
    
    setWindowTitle(tr("Basic Drawing"));

    port_ = "/dev/ttyUSB0";
    // input your portname, ex) Linux: "/dev/ttyUSB0", Windows: "COM1",  Mac: "/dev/tty.SLAB_USBtoUART" or "/dev/tty.usbserial-*"

    serial_.set_option(boost::asio::serial_port_base::baud_rate(baud_rate_));
    boost::asio::write(serial_, boost::asio::buffer("b", 1));
    
    connect(&timer_, SIGNAL(timeout()), this, SLOT(loadData()));
    timer_.start(10);  // msec

}


Window::~Window()
{
  // Stop motor of LDS
  boost::asio::write(serial_, boost::asio::buffer("e", 1));  
}

void Window::loadData()
{
  uint16_t *laser_sensor_data;
  laser_sensor_data = poll();
  //std::cout << *laser_sensor_data << std::endl;
  //std::cout << "sample" << std::endl;

  renderArea->setData(angular_min_, angular_max_, laser_sensor_data);
  repaint();
  renderArea->repaint();
}

uint16_t* Window::poll()
{
  bool      got_scan    = false;
  int       index       = 0;
  uint8_t   start_count = 0;
  uint32_t  motor_speed = 0;
  uint16_t  rpms        = 0;
  static uint16_t range_data[360]     = {0, };
  static uint16_t intensity_data[360] = {0, };
  boost::array<uint8_t, 2520> raw_bytes;
  while (!shutting_down_ && !got_scan)
  {
    // Wait until first data sync of frame: 0xFA, 0xA0
    boost::asio::read(serial_, boost::asio::buffer(&raw_bytes[start_count],1));

    if(start_count == 0)
    {
      if(raw_bytes[start_count] == 0xFA)
      {
        start_count = 1;
      }
    }
    else if(start_count == 1)
    {
      if(raw_bytes[start_count] == 0xA0)
      {
        start_count = 0;

        // Now that entire start sequence has been found, read in the rest of the message
        got_scan = true;

        boost::asio::read(serial_,boost::asio::buffer(&raw_bytes[2], 2518));

        // Read data in sets of 6
        for(uint16_t i = 0; i < raw_bytes.size(); i=i+42)
        {
          if(raw_bytes[i] == 0xFA && raw_bytes[i+1] == (0xA0 + i / 42)) //&& CRC check
          {
            motor_speed += (raw_bytes[i+3] << 8) + raw_bytes[i+2]; //accumulate count for avg. time increment
            rpms=(raw_bytes[i+3]<<8|raw_bytes[i+2])/10;
            for(uint16_t j = i+4; j < i+40; j=j+6)
            {
              index = 6*(i/42) + (j-4-i)/6;

              // Four bytes per reading
              uint8_t byte0 = raw_bytes[j];
              uint8_t byte1 = raw_bytes[j+1];
              uint8_t byte2 = raw_bytes[j+2];
              uint8_t byte3 = raw_bytes[j+3];

              // range and intensity data
              uint16_t intensity = (byte1 << 8) + byte0;
              intensity_data[359-index] = intensity;
              uint16_t range = (byte3 << 8) + byte2;
              range_data[359-index] = range;

              printf ("i[%d]=%d,",359-index, intensity);
              printf ("r[%d]=%d,",359-index, range);
              //printf ("r[%d]=%d,",0, range);
               //printf ("Angular Min: %d \n Angular Max: %d,", angular_min_, angular_max_);
              printf("\n");
	
            }
          }
        }
      }
      else
      {
        start_count = 0;
      }
    }
  }
  return range_data;
}

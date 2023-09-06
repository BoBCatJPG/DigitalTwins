#ifndef WINDOW_H
#define WINDOW_H

#include <QTimer>
#include <QWidget>
#include <boost/asio.hpp>
#include <boost/array.hpp>

class RenderArea;

class Window : public QWidget
{
    Q_OBJECT

public:
    Window();
    ~Window();

private Q_SLOTS:
  void loadData();

   
private:
  uint16_t* poll();
  RenderArea *renderArea;
  QTimer timer_;
  
  qreal angular_min_;
  qreal angular_max_;
  qreal radial_min_;
  qreal radial_max;
  boost::asio::io_service io_;
  std::string port_; ///< @brief The serial port the driver is attached to
  uint32_t baud_rate_; ///< @brief The baud rate for the serial connection
  bool shutting_down_; ///< @brief Flag for whether the driver is supposed to be shutting down or not
  boost::asio::serial_port serial_; ///< @brief Actual serial port object for reading/writing to the LFCD Laser Scanner
  uint16_t motor_speed_; ///< @brief current motor speed as reported by the LFCD.
  
};

#endif // WINDOW_H

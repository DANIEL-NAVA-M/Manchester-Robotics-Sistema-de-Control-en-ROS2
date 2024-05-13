import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import time
import math

class SignalGenerator(Node):
    def __init__(self):
        super().__init__('signal_generator')
        self.publisher_signal = self.create_publisher(Float32, '/signal', 10) #nombre del topico y el tipo de mensaje = crear el publicador(tipo de mensaje, nombre del topico, tamaño del buffer)
        self.publisher_time = self.create_publisher(Float32, '/time', 10) #nombre del topico y el tipo de mensaje = crear el publicador(tipo de mensaje, nombre del topico, tamaño del buffer)
        
        timer_period = 0.5  # 10 Hz
        self.timer = self.create_timer(timer_period, self.timer_callback) #crear el timer (periodo del timer, funcion a llamar)
        self.start_time = self.get_clock().now() #obtener el tiempo actual
        self.get_logger().info('Signal generator node successfully initialized!')

    def timer_callback(self):
        current_time = self.get_clock().now()
        elapsed_time = (current_time - self.start_time).nanoseconds / 1e9
        frecuencia = 0.05
        
        sine_wave = 0.5 * math.sin( 2 * math.pi * 2*0.05 * elapsed_time) + 0.5 * math.sin( 2 * math.pi *0.05 * elapsed_time) #generar la onda sinoidal
        #saw_wave = 1 * (elapsed_time /(1/frecuencia))

        signal_msg = Float32()
        signal_msg.data = sine_wave
        #signal_msg.data = saw_wave
        time_msg = Float32()
        time_msg.data = float(elapsed_time)

        # Publish the messages
        self.publisher_signal.publish(signal_msg)
        self.publisher_time.publish(time_msg)

        # Log the published messages
        self.get_logger().info(f'Published signal: {sine_wave}')
        self.get_logger().info(f'Published time: {elapsed_time}')

def main(args=None):
    rclpy.init(args=args)
    signal_generator = SignalGenerator()
    rclpy.spin(signal_generator)

    # Destroy the node explicitly
    signal_generator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
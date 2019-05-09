package handle.date;

import java.text.NumberFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

public class testDate {

	public static void main(String args[]) {
		
//		彻底明白了Date（日期）Calendar（日历）GregorianCalendar（标准阳历）
//		http://blog.csdn.net/playlaugh2011/article/details/6612445
		
		SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMddHHmmss");
		String date = sdf.format(new Date());
		
		System.out.println(date);
		
		
		/////////////////////////////////////
		NumberFormat f = NumberFormat.getPercentInstance();// 获取格式化类实例
		f.setMinimumFractionDigits(4); // 百分比小数点后两位
		f.format(123123123 * 1.0 / 23423);
		System.out.println(f.format(123123123 * 1.0 / 23423));
		
		//////////////////////////////////////
		
		java.sql.Date nowTime = new java.sql.Date(System.currentTimeMillis());
		SimpleDateFormat sdFormatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		String retStrFormatNowDate = sdFormatter.format(nowTime);
		System.out.println(retStrFormatNowDate);
		System.out.println(System.currentTimeMillis());
	}
	
}

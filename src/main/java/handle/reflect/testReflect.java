package handle.reflect;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class testReflect {

	public static void main(String args[]) throws ClassNotFoundException, IllegalAccessException, IllegalArgumentException, InvocationTargetException, InstantiationException {
		
		Class c = java.lang.Class.forName("handle.reflect.a");
		System.out.println(c.getConstructors());
		System.out.println(c.getName());
		System.out.println(c.getTypeName());
		System.out.println(c.getTypeName());
		System.out.println(c.getClassLoader());
		System.out.println(c.getMethods());
		for( Method method : c.getMethods() )  
		{  
			System.out.println(method.getName());   
//			if( !method.getName().startsWith( "a" ) ) {
//				System.out.println(method.invoke(c.newInstance(), 3));   
//			}
		}
	}
	
}


class a {
	
	public a() {}
	public a(int a) {}
	
	public void b(int x) {}
	public int c(int x) {return x+1;}
}
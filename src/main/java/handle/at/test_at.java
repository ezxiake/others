 package handle.at;

import java.lang.reflect.Field;

// test use the reflection and comment
public class test_at {

	public static void main(String[] args) {
        try {
            Field field = MyBean.class.getDeclaredField("value"); // get value of the member variable `value`
            field.setAccessible(true); // set the `value` to accessible
            if(field.isAnnotationPresent(MyAnnotation.class)){ // whether the member variable have the comment
                MyAnnotation myAnnotation = field.getAnnotation(MyAnnotation.class);// Get the comment `MyAnnotation` that it is defined in member variable `value`
                int value = myAnnotation.value(); // Get the property value that it is defined inside `MyAnnotation` inside of `MyBean`
                MyBean myBean=new MyBean();
                field.setInt(myBean, value); // Assign a value of comment `30` to the member variable `value`
                System.out.println(myBean); // check the result
            }
        } catch (Exception e) {
            e.printStackTrace();
        };
    }
	
}



import api from "../utils/api";

export const PostOrders = async (formData) => {
    try {
        console.log(formData)
      const response = await api.post("/api/order/route", formData); // Replace with your endpoint
      return response.data;
    } catch (error) {
      console.error("Error creating item:", error);
      throw error;
    }
  };
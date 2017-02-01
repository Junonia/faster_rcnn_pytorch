import torch
from torch.autograd import Function
from .._ext import roi_pooling


class RoIPoolFunction(Function):
    def __init__(self, pooled_height, pooled_width, spatial_scale):
        self.pooled_width = int(pooled_width)
        self.pooled_height = int(pooled_height)
        self.spatial_scale = float(spatial_scale)

    def forward(self, features, rois):
        batch_size, num_channels, data_height, data_width = features.size()
        num_rois = rois.size()[0]
        output = torch.zeros(num_rois, num_channels, self.pooled_height, self.pooled_width)
        _features = features.permute(0, 2, 3, 1)
        if not features.is_cuda:
            roi_pooling.roi_pooling_forward(self.pooled_height, self.pooled_width, self.spatial_scale,
                                            _features, rois, output)
        else:
            # TODO: cuda
            roi_pooling.roi_pooling_forward(self.pooled_height, self.pooled_width, self.spatial_scale,
                                            _features.cpu(), rois.cpu(), output)
            output = output.cuda()

        return output

    def backward(self, grad_output):
        # TODO: roi_pooling backward
        # grad_input = grad_output.new()
        # if not grad_output.is_cuda:
        #     my_lib.my_lib_add_backward(grad_output, grad_input)
        # else:
        #     my_lib.my_lib_add_backward_cuda(grad_output, grad_input)
        # return grad_input
        return None